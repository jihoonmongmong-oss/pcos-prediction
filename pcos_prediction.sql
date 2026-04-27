CREATE DATABASE IF NOT EXISTS pcos_prediction;
USE pcos_prediction;

CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT NOT NULL,
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    blood_group VARCHAR(16) NOT NULL,
    menstrual_interval INT NOT NULL,
    weight_gain TINYINT(1) NOT NULL,
    hair_growth TINYINT(1) NOT NULL,
    skin_darkening TINYINT(1) NOT NULL,
    hair_loss TINYINT(1) NOT NULL,
    acne TINYINT(1) NOT NULL,
    fast_food TINYINT(1) NOT NULL,
    exercise TINYINT(1) NOT NULL,
    mood_swings TINYINT(1) NOT NULL,
    periods_regular TINYINT(1) NOT NULL,
    period_length INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    prediction TINYINT(1) NOT NULL,
    probability FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);
