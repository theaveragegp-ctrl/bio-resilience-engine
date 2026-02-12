# Deployment Guide

## Edge Node Deployment (NVIDIA Jetson)

### Hardware Requirements

- NVIDIA Jetson Xavier NX (recommended) or Jetson Nano
- 64GB+ microSD card or NVMe SSD
- USB or CSI camera (1080p @ 30fps minimum)
- Stable power supply (5V 4A for Xavier NX)

### Software Setup

1. **Flash JetPack SDK**
   ```bash
   # Use NVIDIA SDK Manager to flash JetPack 5.1+
   # Includes Ubuntu 20.04, CUDA 11.8, TensorRT 8.6
   ```

2. **Install Dependencies**
   ```bash
   # Clone repository
   git clone https://github.com/bio-resilience/bio-resilience-engine.git
   cd bio-resilience-engine
   
   # Install Python dependencies
   pip3 install -r requirements.txt
   
   # Install jetson-stats for monitoring
   sudo -H pip3 install -U jetson-stats
   ```

3. **Optimize Models with TensorRT**
   ```bash
   # Export YOLOv8-Pose to TensorRT
   python3 scripts/export_tensorrt.py \
     --model models/yolov8n-pose.pt \
     --fp16 \
     --output models/yolov8n-pose.engine
   ```

4. **Configure Edge Node**
   ```bash
   # Edit configuration
   cp .env.example .env
   nano .env
   
   # Set MQTT broker, device ID, camera source
   ```

5. **Run as System Service**
   ```bash
   sudo cp deploy/edge-node.service /etc/systemd/system/
   sudo systemctl enable edge-node
   sudo systemctl start edge-node
   ```

### Performance Optimization

- **Power Mode**: Use MAXN power mode for best performance
  ```bash
  sudo nvpmodel -m 0
  sudo jetson_clocks
  ```

- **GStreamer Acceleration**: Configure hardware-accelerated video capture
  ```python
  gst_pipeline = (
      "nvarguscamerasrc ! "
      "video/x-raw(memory:NVMM), width=1920, height=1080, framerate=30/1 ! "
      "nvvidconv ! video/x-raw, width=640, height=640 ! "
      "videoconvert ! appsink"
  )
  ```

## Cloud Backend Deployment (Kubernetes)

### Prerequisites

- Kubernetes cluster (GKE, EKS, or AKS)
- kubectl configured
- Helm 3+ installed
- PostgreSQL 15+ with TimescaleDB
- Redis cluster
- MQTT broker (Mosquitto or HiveMQ)

### Deployment Steps

1. **Create Namespace**
   ```bash
   kubectl create namespace bio-resilience
   ```

2. **Deploy Secrets**
   ```bash
   kubectl create secret generic api-secrets \
     --from-literal=database-url="postgresql://..." \
     --from-literal=redis-url="redis://..." \
     --from-literal=secret-key="..." \
     -n bio-resilience
   ```

3. **Deploy Database**
   ```bash
   helm install postgres bitnami/postgresql \
     --set auth.postgresPassword=... \
     --set primary.persistence.size=500Gi \
     -n bio-resilience
   
   # Install TimescaleDB extension
   kubectl exec -it postgres-0 -n bio-resilience -- psql -U postgres
   CREATE EXTENSION IF NOT EXISTS timescaledb;
   ```

4. **Deploy Application**
   ```bash
   kubectl apply -f deploy/k8s/deployment.yaml
   kubectl apply -f deploy/k8s/service.yaml
   kubectl apply -f deploy/k8s/ingress.yaml
   ```

5. **Configure Autoscaling**
   ```bash
   kubectl autoscale deployment api \
     --cpu-percent=70 \
     --min=3 \
     --max=20 \
     -n bio-resilience
   ```

### Monitoring Setup

1. **Deploy Prometheus**
   ```bash
   helm install prometheus prometheus-community/kube-prometheus-stack \
     -n monitoring
   ```

2. **Configure Grafana Dashboards**
   ```bash
   kubectl apply -f deploy/grafana/dashboards/
   ```

### Database Migrations

```bash
# Run migrations
kubectl exec -it api-0 -n bio-resilience -- \
  alembic upgrade head
```

## Docker Deployment (Development)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## SSL/TLS Configuration

### Let's Encrypt with Cert-Manager

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f deploy/k8s/cert-issuer.yaml

# Certificate will be automatically provisioned via Ingress annotation
```

## Backup & Recovery

### Database Backups

```bash
# Automated daily backups to GCS
kubectl create cronjob db-backup \
  --image=postgres:15 \
  --schedule="0 2 * * *" \
  --restart=OnFailure \
  -- /backup.sh
```

### Disaster Recovery

1. **Database Restore**
   ```bash
   kubectl exec -it postgres-0 -n bio-resilience -- \
     pg_restore -U postgres -d bio_resilience /backups/latest.dump
   ```

2. **Redis Restore**
   ```bash
   kubectl exec -it redis-0 -n bio-resilience -- \
     redis-cli --rdb /data/dump.rdb
   ```

## Security Hardening

1. **Network Policies**
   ```bash
   kubectl apply -f deploy/k8s/network-policies.yaml
   ```

2. **Pod Security Standards**
   ```bash
   kubectl label namespace bio-resilience \
     pod-security.kubernetes.io/enforce=restricted
   ```

3. **Secrets Management**
   - Use external secrets operator with Vault/AWS Secrets Manager
   - Rotate credentials every 90 days
   - Enable audit logging

## Scaling Guidelines

### Horizontal Scaling

- **API Pods**: Scale based on CPU (target: 70%)
- **Database**: Use read replicas for analytics queries
- **Redis**: Deploy Redis Cluster for > 100GB data

### Vertical Scaling

- **API Pods**: 
  - Request: 500m CPU, 1Gi RAM
  - Limit: 2 CPU, 4Gi RAM

- **PostgreSQL**:
  - Small: 2 vCPU, 8Gi RAM (< 100 subjects)
  - Medium: 4 vCPU, 16Gi RAM (100-500 subjects)
  - Large: 8 vCPU, 32Gi RAM (> 500 subjects)

## Monitoring & Alerts

### Key Metrics

- API response time (p95, p99)
- Database connection pool utilization
- MQTT message throughput
- Edge node connectivity status
- State estimation latency

### Alert Rules

```yaml
- alert: HighAPILatency
  expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
  for: 5m
  annotations:
    summary: "API p95 latency above 500ms"

- alert: EdgeNodeOffline
  expr: up{job="edge-node"} == 0
  for: 2m
  annotations:
    summary: "Edge node {{ $labels.device_id }} is offline"
```

## Troubleshooting

### Common Issues

1. **Edge node inference slow**
   - Check power mode: `sudo nvpmodel -q`
   - Monitor GPU utilization: `tegrastats`
   - Verify TensorRT engine is being used

2. **High API latency**
   - Check database connection pool
   - Verify Redis is responding
   - Review slow query logs

3. **MQTT connection drops**
   - Increase keepalive interval
   - Check network stability
   - Review broker logs

## Support

For deployment assistance, contact devops@bio-resilience.org
