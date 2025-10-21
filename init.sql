-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create database if it doesn't exist (this will be handled by docker-compose)
-- The tables will be created by the application using SQLAlchemy
