import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

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

    st.title("📊 Cuadro de Mandos - Recursos Humanos")
    st.markdown("Análisis demográfico de la plantilla subida vía CSV.")

    # KPIs Principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Empleados", len(df))
    with col2:
        st.metric("Edad Media", round(df['edad'].mean(), 1))
    with col3:
        st.metric("Total Hijos", df['hijos'].sum())
    with col4:
        st.metric("Ciudades", df['ciudad'].nunique())

    st.divider()

    # Gráficos
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Distribución por Sexo")
        fig_sexo = px.pie(df, names='sexo', hole=0.4, 
                          color='sexo', color_discrete_map={'M':'#1f77b4', 'F':'#ff7f0e'})
        st.plotly_chart(fig_sexo, use_container_width=True)

    with row1_col2:
        st.subheader("Empleados por Ciudad")
        city_counts = df['ciudad'].value_counts().reset_index()
        fig_city = px.bar(city_counts, x='ciudad', y='count', 
                          labels={'count':'Nº Empleados', 'ciudad':'Ciudad'},
                          color='count', color_continuous_scale='Viridis')
        st.plotly_chart(fig_city, use_container_width=True)

    st.divider()

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("Distribución de Edades")
        fig_age = px.histogram(df, x='edad', nbins=15, 
                               marginal="box", title="Histograma de Edad")
        st.plotly_chart(fig_age, use_container_width=True)

    with row2_col2:
        st.subheader("Relación Edad vs Hijos")
        fig_scatter = px.scatter(df, x='edad', y='hijos', color='sexo',
                                 size='hijos', hover_data=['nombre', 'apellido'])
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Tabla de datos crudos
    st.divider()
    st.subheader("Listado Detallado")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.info("Asegúrate de que los contenedores de Docker están activos y los datos cargados.")
