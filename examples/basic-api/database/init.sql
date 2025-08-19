-- Database initialization script for basic-api
-- This script runs when the PostgreSQL container starts for the first time

-- Create database if it doesn't exist
SELECT 'CREATE DATABASE basic-api'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'basic-api')\gexec

-- Connect to the database
\c basic-api;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create a simple health check table
CREATE TABLE IF NOT EXISTS health_check (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'healthy',
    last_check TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    message TEXT
);

-- Insert initial health check record
INSERT INTO health_check (service_name, status, message) 
VALUES ('basic-api', 'healthy', 'Database initialized successfully')
ON CONFLICT DO NOTHING;

-- Grant permissions to postgres user
GRANT ALL PRIVILEGES ON DATABASE basic-api TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;