-- Database initialization script for Bio-Resilience Engine
-- Creates TimescaleDB extension and initial schema

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create database if not exists (handled by Docker env vars)
-- CREATE DATABASE bio_resilience;

-- Connect to the database
\c bio_resilience;

-- Subjects table
CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    age INTEGER CHECK (age >= 18 AND age <= 100),
    weight_kg FLOAT CHECK (weight_kg > 0),
    height_cm FLOAT CHECK (height_cm > 0),
    baseline_hr FLOAT DEFAULT 70.0,
    created_at TIMESTAMP DEFAULT NOW(),
    active BOOLEAN DEFAULT true
);

CREATE INDEX IF NOT EXISTS idx_subjects_external_id ON subjects(external_id);
CREATE INDEX IF NOT EXISTS idx_subjects_active ON subjects(active);

-- Biosignal measurements (will be converted to hypertable)
CREATE TABLE IF NOT EXISTS biosignal_measurements (
    id BIGSERIAL,
    subject_id INTEGER REFERENCES subjects(id),
    timestamp TIMESTAMP NOT NULL,
    heart_rate FLOAT,
    respiratory_rate FLOAT,
    spo2 FLOAT,
    temperature FLOAT,
    accel_x FLOAT,
    accel_y FLOAT,
    accel_z FLOAT,
    device_id VARCHAR(255),
    metadata JSONB,
    PRIMARY KEY (id, timestamp)
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('biosignal_measurements', 'timestamp', 
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

CREATE INDEX IF NOT EXISTS idx_biosignal_subject_time 
    ON biosignal_measurements (subject_id, timestamp DESC);

-- Pose estimates (will be converted to hypertable)
CREATE TABLE IF NOT EXISTS pose_estimates (
    id BIGSERIAL,
    subject_id INTEGER REFERENCES subjects(id),
    timestamp TIMESTAMP NOT NULL,
    keypoints JSONB,
    activity_label VARCHAR(100),
    activity_confidence FLOAT,
    edge_node_id VARCHAR(255),
    inference_latency_ms FLOAT,
    metadata JSONB,
    PRIMARY KEY (id, timestamp)
);

SELECT create_hypertable('pose_estimates', 'timestamp',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

CREATE INDEX IF NOT EXISTS idx_pose_subject_time 
    ON pose_estimates (subject_id, timestamp DESC);

-- Physiological state estimates
CREATE TABLE IF NOT EXISTS physiological_states (
    id BIGSERIAL,
    subject_id INTEGER REFERENCES subjects(id),
    timestamp TIMESTAMP NOT NULL,
    heart_rate FLOAT,
    respiratory_rate FLOAT,
    activity_level FLOAT,
    fatigue_index FLOAT,
    stress_level FLOAT,
    resilience_score FLOAT,
    covariance_matrix JSONB,
    source_modalities JSONB,
    confidence FLOAT,
    PRIMARY KEY (id, timestamp)
);

SELECT create_hypertable('physiological_states', 'timestamp',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

CREATE INDEX IF NOT EXISTS idx_physio_subject_time 
    ON physiological_states (subject_id, timestamp DESC);

-- Create continuous aggregate for 5-minute rollups
CREATE MATERIALIZED VIEW IF NOT EXISTS biosignal_5min
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('5 minutes', timestamp) AS bucket,
    subject_id,
    AVG(heart_rate) as avg_hr,
    STDDEV(heart_rate) as stddev_hr,
    AVG(respiratory_rate) as avg_rr,
    COUNT(*) as sample_count
FROM biosignal_measurements
GROUP BY bucket, subject_id
WITH NO DATA;

-- Add retention policy (keep 90 days)
SELECT add_retention_policy('biosignal_measurements', INTERVAL '90 days', if_not_exists => TRUE);
SELECT add_retention_policy('pose_estimates', INTERVAL '90 days', if_not_exists => TRUE);
SELECT add_retention_policy('physiological_states', INTERVAL '90 days', if_not_exists => TRUE);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
