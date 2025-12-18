import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.express as px
import os
import subprocess
import time
from load_csv import load_csv_to_mysql

# Función para inicializar todo el entorno si es necesario
def init_environment():
    try:
        # 1. Intentar conectar para ver si la DB existe
        engine_check = create_engine("mysql+pymysql://root:password@localhost:3306/")
        with engine_check.connect() as conn:
            result = conn.execute(text("SHOW DATABASES LIKE 'rrhh'")).fetchone()
            if result:
                return # Si existe, no hacemos nada
    except Exception:
        # Si falla la conexión, asumimos que Docker no está levantado o la DB no existe
        pass

    st.info("Iniciando infraestructura y base de datos por primera vez...")
    
    # 2. Levantar Docker
    subprocess.run(["docker-compose", "up", "-d"], check=True)
    
    # 3. Esperar a que MySQL esté listo (polling)
    max_retries = 30
    connected = False
    while max_retries > 0 and not connected:
        try:
            engine_check = create_engine("mysql+pymysql://root:password@localhost:3306/rrhh")
            with engine_check.connect() as conn:
                connected = True
        except Exception:
            time.sleep(2)
            max_retries -= 1
    
    if connected:
        # 4. Cargar datos iniciales
        load_csv_to_mysql('personas.csv', 'personas')
        st.success("Entorno inicializado correctamente.")
    else:
        st.error("No se pudo conectar a la base de datos tras iniciar Docker.")

# Ejecutar inicialización
init_environment()

# Configuración de la página
st.set_page_config(page_title="Dashboard RRHH", layout="wide")

# Conexión a la base de datos
@st.cache_resource
def get_engine():
    return create_engine("mysql+pymysql://root:password@localhost:3306/rrhh")

engine = get_engine()

# Carga de datos
@st.cache_data
def load_data():
    query = "SELECT * FROM personas"
    return pd.read_sql(query, engine)

try:
    df = load_data()

    st.title("📊 Análisis Estratégico de Recursos Humanos")
    st.markdown("Prototipo de Business Intelligence para la gestión dinámica de talento.")

    # Estilo de KPIs con CSS personalizado
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            font-size: 35px;
            color: #636EFA;
        }
        [data-testid="stMetricLabel"] {
            font-weight: bold;
            text-transform: uppercase;
        }
        div.block-container {
            padding-top: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)

    # KPIs Principales en tarjetas resaltadas
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Plantilla Total", f"{len(df)} pers.")
    kpi2.metric("Promedio Edad", f"{round(df['edad'].mean(), 1)} años")
    kpi3.metric("Carga Familiar", f"{int(df['hijos'].sum())} hijos")
    kpi4.metric("Dispersión Geográfica", f"{df['ciudad'].nunique()} sedes")

    st.divider()

    # Gráficos
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("#### 🚻 Distribución por Sexo")
        fig_sexo = px.pie(df, names='sexo', hole=0.5,
                          color='sexo', color_discrete_map={'M':'#00CC96', 'F':'#EF553B'},
                          template="plotly_dark")
        fig_sexo.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
        st.plotly_chart(fig_sexo, width='stretch')

    with row1_col2:
        st.markdown("#### 📍 Empleados por Ciudad")
        city_counts = df['ciudad'].value_counts().reset_index()
        fig_city = px.bar(city_counts, x='ciudad', y='count',
                          labels={'count':'Nº Empleados', 'ciudad':'Ciudad'},
                          color='count', color_continuous_scale='GnBu',
                          template="plotly_dark")
        fig_city.update_layout(margin=dict(t=20, b=20, l=0, r=0), xaxis_title=None)
        st.plotly_chart(fig_city, width='stretch')

    st.divider()

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("#### 🎂 Pirámide de Edades")
        fig_age = px.histogram(df, x='edad', nbins=15,
                               marginal="violin",
                               color_discrete_sequence=['#636EFA'],
                               template="plotly_dark")
        fig_age.update_layout(margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig_age, width='stretch')

    with row2_col2:
        st.markdown("#### 👨‍👩‍👧 Relación Edad vs Hijos")
        fig_scatter = px.scatter(df, x='edad', y='hijos', color='sexo',
                                 size='hijos', hover_data=['nombre', 'apellido'],
                                 color_discrete_map={'M':'#00CC96', 'F':'#EF553B'},
                                 template="plotly_dark")
        fig_scatter.update_layout(margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig_scatter, width='stretch')

    # Tabla de datos crudos
    st.divider()
    st.subheader("Listado Detallado")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.info("Asegúrate de que los contenedores de Docker están activos y los datos cargados.")
