-- Initialization SQL run on first startup
-- Add extensions required for production here (pgcrypto, pgvector, etc.)
-- NOTE: Installing pgvector may require a custom image or installing extension packages.

-- Example (may fail on plain postgres image if extension not present):
-- CREATE EXTENSION IF NOT EXISTS vector;

-- Create a database role for migrations (optional)
-- CREATE ROLE deployer WITH LOGIN PASSWORD 'deployer_pass';
