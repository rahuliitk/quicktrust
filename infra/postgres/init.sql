-- Create keycloak database for Keycloak service
CREATE DATABASE keycloak;

-- Enable extensions on the main opencomply database
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
