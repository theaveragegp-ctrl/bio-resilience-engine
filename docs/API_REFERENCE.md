# Bio-Resilience Engine - API Reference

## Base URL

```
Production: https://api.bio-resilience.org
Staging: https://staging-api.bio-resilience.org
Local: http://localhost:8000
```

## Authentication

All API endpoints require JWT authentication (except health check).

### Obtain Token

```http
POST /api/v1/auth/token
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "secure_password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

Use token in subsequent requests:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Endpoints

### Health & Status

#### GET /api/v1/health/

Check system health status.

**Response:**
```json
{
  "status": "operational",
  "timestamp": "2024-01-30T12:00:00Z",
  "version": "0.4.2",
  "database_connected": true,
  "redis_connected": true,
  "mqtt_connected": true,
  "active_edge_nodes": 12,
  "total_subjects": 47
}
```

### Sensor Fusion

#### POST /api/v1/fusion/ingest/biosignal

Ingest biosignal data from wearable device.

**Request:**
```json
{
  "subject_id": "sub_001",
  "timestamp": 1706616000.0,
  "heart_rate": 145.0,
  "respiratory_rate": 22.0,
  "spo2": 97.5,
  "temperature": 37.2,
  "accel_magnitude": 1.8,
  "device_id": "watch_001"
}
```

**Response:**
```json
{
  "status": "ingested",
  "subject_id": "sub_001",
  "timestamp": 1706616000.0,
  "fusion_triggered": true
}
```

#### POST /api/v1/fusion/ingest/pose

Ingest pose estimation data from edge node.

**Request:**
```json
{
  "subject_id": "sub_001",
  "timestamp": 1706616000.0,
  "keypoints": [[100.0, 200.0, 0.95], ...],  // 17x3 array
  "activity_label": "running",
  "activity_confidence": 0.92,
  "edge_node_id": "jetson_001"
}
```

#### GET /api/v1/fusion/state/{subject_id}

Retrieve current physiological state estimate.

**Response:**
```json
{
  "subject_id": "sub_001",
  "timestamp": "2024-01-30T12:00:00Z",
  "heart_rate": 145.2,
  "respiratory_rate": 21.8,
  "activity_level": 8.5,
  "fatigue_index": 0.42,
  "stress_level": 0.38,
  "resilience_score": 73.5,
  "confidence": 0.89
}
```

#### GET /api/v1/fusion/state/{subject_id}/history

Retrieve historical state estimates.

**Query Parameters:**
- `start_time` (ISO 8601): Start of time range
- `end_time` (ISO 8601): End of time range
- `limit` (int): Maximum records (default: 100, max: 1000)

**Response:**
```json
[
  {
    "subject_id": "sub_001",
    "timestamp": "2024-01-30T12:00:00Z",
    "heart_rate": 145.2,
    ...
  },
  ...
]
```

### Physiological Analysis

#### GET /api/v1/analysis/resilience/{subject_id}

Calculate comprehensive resilience score.

**Response:**
```json
{
  "subject_id": "sub_001",
  "timestamp": "2024-01-30T12:00:00Z",
  "overall_score": 73.5,
  "cardiovascular_score": 78.2,
  "metabolic_score": 71.3,
  "recovery_score": 69.8,
  "stress_adaptation_score": 75.1,
  "confidence": 0.87
}
```

#### GET /api/v1/analysis/fatigue/predict/{subject_id}

Predict future fatigue levels.

**Query Parameters:**
- `horizon_minutes` (int): Prediction horizon (default: 60, max: 300)

**Response:**
```json
{
  "subject_id": "sub_001",
  "current_fatigue": 0.42,
  "predicted_fatigue_30min": 0.58,
  "predicted_fatigue_60min": 0.71,
  "time_to_critical_fatigue_min": 87.3,
  "recommended_rest_duration_min": 25.0,
  "prediction_confidence": 0.82
}
```

#### GET /api/v1/analysis/anomaly/detect/{subject_id}

Detect physiological anomalies.

**Query Parameters:**
- `lookback_minutes` (int): Analysis window (default: 30, max: 1440)

**Response:**
```json
[
  {
    "subject_id": "sub_001",
    "timestamp": "2024-01-30T11:45:00Z",
    "anomaly_detected": true,
    "anomaly_score": 0.87,
    "affected_signals": ["heart_rate", "respiratory_rate"],
    "severity": "medium",
    "description": "Sudden heart rate spike inconsistent with activity level"
  }
]
```

#### GET /api/v1/analysis/recovery/estimate/{subject_id}

Estimate recovery time to baseline.

**Response:**
```json
{
  "subject_id": "sub_001",
  "current_state": "elevated",
  "baseline_hr": 68.0,
  "current_hr": 145.0,
  "estimated_recovery_time_min": 32.5,
  "recovery_phase": "active_recovery",
  "recommendations": [
    "Maintain light activity for 10 minutes",
    "Hydrate with 250ml water",
    "Monitor HR until below 90 bpm"
  ]
}
```

### Subject Management

#### POST /api/v1/subjects/

Create new subject.

**Request:**
```json
{
  "external_id": "HOSPITAL_12345",
  "name": "John Doe",
  "age": 35,
  "weight_kg": 75.0,
  "height_cm": 175.0,
  "baseline_hr": 65.0
}
```

**Response:**
```json
{
  "id": 1,
  "external_id": "HOSPITAL_12345",
  "name": "John Doe",
  "age": 35,
  "weight_kg": 75.0,
  "height_cm": 175.0,
  "baseline_hr": 65.0,
  "created_at": "2024-01-30T12:00:00Z",
  "active": true
}
```

#### GET /api/v1/subjects/{subject_id}

Retrieve subject details.

#### GET /api/v1/subjects/

List all subjects.

**Query Parameters:**
- `active_only` (bool): Filter active subjects (default: true)
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Maximum records (default: 100)

## Rate Limits

- **Standard tier**: 100 requests/minute
- **Premium tier**: 1000 requests/minute
- **Enterprise tier**: Unlimited

Rate limit headers:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1706616060
```

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message",
  "status_code": 400,
  "timestamp": "2024-01-30T12:00:00Z"
}
```

### Common Status Codes

- `200 OK`: Request succeeded
- `201 Created`: Resource created
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Temporary service disruption

## Webhooks

Subscribe to real-time events via webhooks.

### Available Events

- `state.updated`: New physiological state estimate
- `anomaly.detected`: Anomaly detected in biosignals
- `fatigue.critical`: Subject approaching critical fatigue
- `subject.created`: New subject registered

### Webhook Payload

```json
{
  "event": "anomaly.detected",
  "timestamp": "2024-01-30T12:00:00Z",
  "data": {
    "subject_id": "sub_001",
    "anomaly_score": 0.87,
    "severity": "high"
  }
}
```

## SDK Examples

### Python

```python
import requests

API_BASE = "https://api.bio-resilience.org"
TOKEN = "your_jwt_token"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Ingest biosignal
response = requests.post(
    f"{API_BASE}/api/v1/fusion/ingest/biosignal",
    json={
        "subject_id": "sub_001",
        "timestamp": 1706616000.0,
        "heart_rate": 145.0,
        "device_id": "watch_001"
    },
    headers=headers
)

# Get current state
response = requests.get(
    f"{API_BASE}/api/v1/fusion/state/sub_001",
    headers=headers
)
state = response.json()
print(f"Resilience: {state['resilience_score']}")
```

### Swift (WatchOS)

```swift
import BioResilienceSDK

let sdk = BioResilienceSDK(apiEndpoint: "https://api.bio-resilience.org")
sdk.startMonitoring(subjectID: "sub_001")
```

## Support

- **Documentation**: https://docs.bio-resilience.org
- **Status Page**: https://status.bio-resilience.org
- **Support Email**: support@bio-resilience.org
- **GitHub Issues**: https://github.com/bio-resilience/bio-resilience-engine/issues
