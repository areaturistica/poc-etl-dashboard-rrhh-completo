# PoC: Solución Integral de Gestión de RRHH (ETL + Dashboard)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Esta **Prueba de Concepto (PoC)** demuestra una solución completa de ingeniería de datos para el área de Recursos Humanos. El proyecto abarca desde la creación automática de la infraestructura hasta el procesamiento de datos (ETL) y su visualización final en un cuadro de mandos interactivo.

## 🚀 Componentes de la PoC

1.  **Infraestructura (Docker)**: Despliegue automatizado de un entorno con MySQL 8.0 y phpMyAdmin.
2.  **Proceso ETL (Python)**: Script dinámico que lee datos desde archivos CSV, realiza la limpieza/preparación y los carga en la base de datos relacional.
3.  **Cuadro de Mandos (Streamlit)**: Informe interactivo para el análisis demográfico y de métricas clave (KPIs) de la plantilla.

## 🛠️ Características Técnicas

*   **Carga Dinámica**: El script de carga detecta automáticamente las columnas del CSV, facilitando la escalabilidad.
*   **Base de Datos**: Esquema `rrhh` optimizado con índices para búsquedas rápidas por nombre y apellido.
*   **Visualización**: Gráficos interactivos de distribución de edades, género y dispersión familiar.
*   **Aislamiento**: Configuración mediante entornos virtuales de Python (`venv`).

## 📋 Requisitos Previos

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.
*   [Python 3.12](https://www.python.org/downloads/) o superior.

## 📂 Estructura del Proyecto

*   `personas.csv`: Datos de ejemplo anonimizados.
*   `docker-compose.yml`: Orquestación de servicios (Base de Datos y Administrador).
*   `init.sql`: Script DDL para la inicialización de la base de datos.
*   `load_csv.py`: Lógica ETL en Python.
*   `app.py`: Aplicación web del Dashboard con Streamlit.
*   `LICENSE`: Licencia MIT de código abierto.

## ⏱️ Guía de Inicio Rápido

### 1. Levantar la Infraestructura
Inicia los servicios de base de datos:

```bash
docker-compose up -d
```

*   **phpMyAdmin**: [http://localhost:8080](http://localhost:8080) (Usuario: `root` / Pass: `password`)
*   **MySQL Host**: `localhost:3306`

### 2. Configurar el Entorno de Python
Activa el entorno e instala las dependencias:

```bash
# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install mysql-connector-python streamlit pandas plotly sqlalchemy pymysql
```

### 3. Ejecutar el Proceso ETL
Carga los datos del CSV a la base de datos:

```bash
python load_csv.py
```

### 4. Lanzar el Cuadro de Mandos
Visualiza el informe final:

```bash
streamlit run app.py
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
**Repositorio Oficial**: [https://github.com/areaturistica/poc-etl-dashboard-rrhh-completo](https://github.com/areaturistica/poc-etl-dashboard-rrhh-completo)
