# Changelog

All notable changes to the Bio-Resilience Engine will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.2] - 2024-01-30

### Added
- Adaptive Kalman filter tuning based on innovation statistics
- WatchOS SDK background delivery support
- Anomaly detection using Isolation Forest
- Recovery time estimation endpoint
- Grafana dashboards for real-time monitoring
- Integration tests for complete data pipeline
- API rate limiting per client tier

### Changed
- Upgraded PyTorch to 2.1.2 for improved CUDA efficiency
- Optimized database queries with TimescaleDB continuous aggregates
- Enhanced MQTT reconnection logic with exponential backoff
- Updated YOLO model to v8.1 for better accuracy

### Fixed
- Memory leak in Kalman filter tracking
- Race condition in MQTT message handling
- Incorrect respiratory rate calculation from chest expansion
- Edge node clock drift causing timestamp misalignment

### Security
- Added JWT token rotation mechanism
- Implemented certificate pinning in WatchOS SDK
- Enhanced input validation for all API endpoints

## [0.4.1] - 2024-01-15

### Added
- Multi-subject tracking on single edge node
- Predictive fatigue modeling with LSTM
- Redis caching for frequently accessed states
- Prometheus metrics export

### Changed
- Migrated from SQLite to PostgreSQL + TimescaleDB
- Refactored Bayesian fusion to use UKF instead of EKF
- Improved activity classification accuracy (87% → 92%)

### Fixed
- Edge node crashes during rapid activity transitions
- Negative resilience scores for edge cases
- API timeout issues under high load

## [0.4.0] - 2024-01-01

### Added
- Initial public release
- YOLOv8-Pose integration for edge inference
- FastAPI backend with sensor fusion
- WatchOS SDK for biosignal acquisition
- Docker Compose deployment configuration
- Comprehensive documentation

### Performance
- Edge inference: 28ms latency @ 30 FPS
- Cloud API: 45ms p95 response time
- End-to-end: 87ms total latency

## [0.3.0] - 2023-12-15 (Internal Beta)

### Added
- Prototype Bayesian fusion engine
- Basic edge inference pipeline
- Database schema design
- Initial API endpoints

### Known Issues
- Kalman filter divergence during occlusions
- Limited to single-subject scenarios
- No authentication/authorization

## [0.2.0] - 2023-11-01 (Alpha)

### Added
- Proof-of-concept pose estimation
- Preliminary biosignal integration
- Basic data visualization

## [0.1.0] - 2023-09-15 (Research Prototype)

### Added
- Initial research codebase
- Offline data processing scripts
- Evaluation on benchmark datasets
