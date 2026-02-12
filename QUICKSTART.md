# Bio-Resilience Engine - Quick Start Guide

## 🚀 5-Minute Demo

Get the system running in 5 minutes with Docker.

### Prerequisites

- Docker 20.10+ with Docker Compose
- 8GB+ RAM available
- 10GB+ disk space

### Start the System

```bash
# 1. Clone repository
git clone https://github.com/bio-resilience/bio-resilience-engine.git
cd bio-resilience-engine

# 2. Start all services
docker-compose up -d

# 3. Wait for services to initialize (~30 seconds)
docker-compose logs -f api

# Watch for: "Application startup complete"
```

### Verify Deployment

```bash
# Check system health
curl http://localhost:8000/api/v1/health/ | jq

# Expected response:
{
  "status": "operational",
  "database_connected": true,
  "redis_connected": true,
  "mqtt_connected": true
}
```

### Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **API Documentation** | http://localhost:8000/api/docs | None (public) |
| **Grafana Dashboards** | http://localhost:3000 | admin / admin |
| **Prometheus Metrics** | http://localhost:9090 | None |

### Test the API

#### 1. Create a Subject

```bash
curl -X POST http://localhost:8000/api/v1/subjects/ \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "DEMO_001",
    "name": "Demo Subject",
    "age": 35,
    "weight_kg": 75.0,
    "height_cm": 175.0,
    "baseline_hr": 65.0
  }'
```

#### 2. Ingest Biosignal Data

```bash
curl -X POST http://localhost:8000/api/v1/fusion/ingest/biosignal \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id": "DEMO_001",
    "timestamp": '$(date +%s.%N)',
    "heart_rate": 145.0,
    "respiratory_rate": 22.0,
    "spo2": 97.5,
    "accel_magnitude": 1.8,
    "device_id": "watch_001"
  }'
```

#### 3. Query Current State

```bash
curl http://localhost:8000/api/v1/fusion/state/DEMO_001 | jq
```

#### 4. Get Resilience Score

```bash
curl http://localhost:8000/api/v1/analysis/resilience/DEMO_001 | jq
```

### Explore Interactive Docs

Visit http://localhost:8000/api/docs for full API documentation with **Try it out** functionality.

## 🎯 What's Running?

```
┌─────────────────────────────────────────┐
│         Your Local Stack                │
├─────────────────────────────────────────┤
│ ✓ FastAPI Backend (port 8000)          │
│ ✓ PostgreSQL + TimescaleDB (5432)      │
│ ✓ Redis Cache (6379)                   │
│ ✓ MQTT Broker (1883)                   │
│ ✓ Kafka (9092)                         │
│ ✓ Prometheus (9090)                    │
│ ✓ Grafana (3000)                       │
│ ✓ Edge Node Simulator                  │
└─────────────────────────────────────────┘
```

## 🧪 Run Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run test suite
pytest tests/ -v --cov=src

# Run only fast tests (skip integration)
pytest tests/ -v -m "not slow"
```

## 📊 View Monitoring

### Grafana Dashboards

1. Open http://localhost:3000
2. Login: `admin` / `admin`
3. Navigate to **Dashboards** → **Bio-Resilience**
4. View real-time metrics:
   - API request rate
   - Response latency (p50, p95, p99)
   - Database connection pool
   - Active edge nodes
   - Subject count

### Prometheus Metrics

Visit http://localhost:9090 and try these queries:

```promql
# API request rate
rate(http_requests_total[5m])

# API latency p95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Database connections
pg_stat_database_numbackends{datname="bio_resilience"}
```

## 🎮 Simulate Edge Node

The stack includes a simulated edge node that publishes mock pose data:

```bash
# View edge simulator logs
docker-compose logs -f edge-simulator

# You should see:
# "Published pose data for 2 subjects"
# "Inference time: 28.3ms"
```

## 🔧 Development Setup

For local development without Docker:

```bash
# 1. Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env with your configuration

# 4. Start services (requires local Postgres, Redis, MQTT)
make api-run

# 5. In another terminal, start edge node
make edge-run
```

## 📱 WatchOS SDK

To use the WatchOS SDK in your Apple Watch app:

```swift
import BioResilienceSDK

// Initialize SDK
let sdk = BioResilienceSDK(apiEndpoint: "http://localhost:8000")

// Request HealthKit authorization
sdk.requestAuthorization { success, error in
    if success {
        // Start monitoring
        sdk.startMonitoring(subjectID: "DEMO_001")
    }
}
```

## 🛑 Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

## 📚 Next Steps

1. **Read the Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. **Review API Reference**: [docs/API_REFERENCE.md](docs/API_REFERENCE.md)
3. **Study Technical Spec**: [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md)
4. **Deployment Guide**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
5. **Explore Code**:
   - Edge processing: `src/edge_node/`
   - Cloud backend: `src/cloud_fusion/`
   - WatchOS SDK: `src/wearable_sdk/`

## ❓ Troubleshooting

### Services won't start

```bash
# Check Docker resources (need 8GB+ RAM)
docker stats

# View service logs
docker-compose logs api
docker-compose logs postgres
```

### API returns 503 Service Unavailable

```bash
# Database may still be initializing
docker-compose logs postgres

# Wait for: "database system is ready to accept connections"
```

### Cannot connect to localhost:8000

```bash
# Verify API is running
docker-compose ps

# Check if port is in use
lsof -i :8000

# Restart API service
docker-compose restart api
```

### Tests failing

```bash
# Ensure no services are running on default ports
docker-compose down

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests in isolated environment
pytest tests/ -v --tb=short
```

## 💬 Support

- **Documentation**: Full docs in `docs/` directory
- **Issues**: https://github.com/bio-resilience/bio-resilience-engine/issues
- **Email**: support@bio-resilience.org

## 🎉 Success!

You now have a complete bio-resilience monitoring system running locally!

**Try this complete workflow**:

1. ✅ Create subject (DEMO_001)
2. ✅ Ingest biosignal data from "wearable"
3. ✅ Simulate pose data from "edge node"
4. ✅ Query fused physiological state
5. ✅ Get resilience score
6. ✅ View predictions (fatigue, anomalies)
7. ✅ Monitor system metrics in Grafana

---

**Ready for production?** See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for Kubernetes deployment.
