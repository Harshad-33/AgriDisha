-- ====================================================
-- AgriDisha Database Schema (MySQL 8.0+)
-- Smart Agriculture Recommendation System
-- ====================================================

CREATE DATABASE IF NOT EXISTS agridisha_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE agridisha_db;

-- ----------------------------------------------------
-- Table: users
-- ----------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(60) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    location VARCHAR(100),
    role VARCHAR(20) NOT NULL DEFAULT 'ROLE_USER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------
-- Table: crop_predictions
-- ----------------------------------------------------
CREATE TABLE IF NOT EXISTS crop_predictions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NULL,
    nitrogen DOUBLE NOT NULL,
    phosphorous DOUBLE NOT NULL,
    potassium DOUBLE NOT NULL,
    temperature DOUBLE NOT NULL,
    humidity DOUBLE NOT NULL,
    ph_level DOUBLE NOT NULL,
    rainfall DOUBLE NOT NULL,
    city VARCHAR(100),
    predicted_crop VARCHAR(100) NOT NULL,
    confidence_score DOUBLE DEFAULT 0.95,
    model_used VARCHAR(100) DEFAULT 'RandomForestClassifier',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_crop_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    INDEX idx_crop_user_id (user_id),
    INDEX idx_crop_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------
-- Table: fertilizer_recommendations
-- ----------------------------------------------------
CREATE TABLE IF NOT EXISTS fertilizer_recommendations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NULL,
    crop_name VARCHAR(100) NOT NULL,
    nitrogen DOUBLE NOT NULL,
    phosphorous DOUBLE NOT NULL,
    potassium DOUBLE NOT NULL,
    soil_status VARCHAR(100) NOT NULL,
    primary_recommendation TEXT,
    chemical_fertilizers TEXT,
    organic_alternatives TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fertilizer_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    INDEX idx_fertilizer_user_id (user_id),
    INDEX idx_fertilizer_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------
-- Table: disease_predictions
-- ----------------------------------------------------
CREATE TABLE IF NOT EXISTS disease_predictions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NULL,
    image_filename VARCHAR(255),
    crop_name VARCHAR(100) NOT NULL,
    disease_name VARCHAR(150) NOT NULL,
    health_status VARCHAR(50) NOT NULL,
    confidence_score DOUBLE DEFAULT 0.94,
    severity VARCHAR(50),
    cause TEXT,
    symptoms TEXT,
    prevention_advice TEXT,
    treatment_advice TEXT,
    supplement_advice TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_disease_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    INDEX idx_disease_user_id (user_id),
    INDEX idx_disease_created_at (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------
-- Initial Demo User Seed (Password: password123)
-- ----------------------------------------------------
INSERT IGNORE INTO users (username, email, password, full_name, location, role)
VALUES ('farmer_john', 'farmer@agridisha.com', '$2a$10$7R0wU/vP9tJEvN4yVqXkSeK.uG90v0EwGqC9G5fV.VzK6H6tL7Cae', 'John Agro', 'Maharashtra, India', 'ROLE_USER');
