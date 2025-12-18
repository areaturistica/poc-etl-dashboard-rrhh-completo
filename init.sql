CREATE DATABASE IF NOT EXISTS rrhh;
USE rrhh;

CREATE TABLE IF NOT EXISTS personas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    edad INT,
    ciudad VARCHAR(100),
    hijos INT DEFAULT 0,
    sexo CHAR(1),
    INDEX idx_nombre_apellido (nombre, apellido)
);
