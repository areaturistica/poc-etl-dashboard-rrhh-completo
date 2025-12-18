# Proyecto de Gestión de RRHH - Carga Dinámica de Datos

Este proyecto automatiza la creación de un entorno de base de datos MySQL mediante Docker y proporciona herramientas para cargar datos de personas desde un archivo CSV de forma dinámica utilizando Python.

## Características

*   **Generación de Datos**: Archivo CSV con 80 registros de personas de ejemplo.
*   **Infraestructura**: Entorno Dockerizado con MySQL 8.0 y phpMyAdmin.
*   **Base de Datos**: Esquema `rrhh` con tabla `personas` indexada por nombre y apellido.
*   **Automatización**: Script de Python para la carga dinámica de datos, detectando automáticamente las columnas del CSV.
*   **Entorno Aislado**: Configuración de entorno virtual de Python (`venv`).

## Requisitos Previos

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.
*   [Python 3.12](https://www.python.org/downloads/) o superior.

## Estructura del Proyecto

*   `personas.csv`: Contiene los datos de ejemplo (80 registros).
*   `docker-compose.yml`: Configuración de los servicios MySQL y phpMyAdmin.
*   `init.sql`: Script de inicialización de la base de datos (DDL).
*   `load_csv.py`: Script de Python para importar los datos.
*   `venv/`: Entorno virtual de Python (excluido en git).

## Guía de Inicio Rápido

### 1. Levantar la infraestructura
Ejecuta el siguiente comando para iniciar la base de datos y phpMyAdmin:

```bash
docker-compose up -d
```

*   **phpMyAdmin**: [http://localhost:8080](http://localhost:8080)
    *   **Usuario**: `root`
    *   **Contraseña**: `password`
*   **MySQL Host**: `localhost:3306`

### 2. Configurar el entorno de Python
Activa el entorno virtual e instala las dependencias necesarias:

```bash
# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install mysql-connector-python streamlit pandas plotly sqlalchemy pymysql
```

### 3. Cargar los datos
Ejecuta el script de carga para importar los registros del CSV a la tabla de MySQL:

```bash
python load_csv.py
```

### 4. Lanzar el Cuadro de Mandos (Dashboard)
Para visualizar los datos en el sistema web simplificado:

```bash
streamlit run app.py
```

El dashboard se abrirá automáticamente en tu navegador (normalmente en [http://localhost:8501](http://localhost:8501)).

## Detalles Técnicos de la Base de Datos

El esquema se crea automáticamente al iniciar el contenedor mediante el archivo `init.sql`:

```sql
CREATE DATABASE IF NOT EXISTS rrhh;
USE rrhh;

CREATE TABLE IF NOT EXISTS personas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    edad INT,
    ciudad VARCHAR(100),
    INDEX idx_nombre_apellido (nombre, apellido) -- Optimización para búsquedas
);
```
