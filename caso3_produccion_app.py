# ══════════════════════════════════════════════════════════════
# APP STREAMLIT — DASHBOARD PRODUCCIÓN INDUSTRIAL
# Desarrollado por:
# Maria Paula Benavides y Nicolás Clavijo Hernández
# ══════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import plotly.express as px

# ══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PÁGINA
# ══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title='Dashboard Producción Industrial',
    page_icon='🏭',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ══════════════════════════════════════════════════════════════
# ESTILOS PERSONALIZADOS
# ══════════════════════════════════════════════════════════════

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
}

h1, h2, h3{
    color:#c2185b;
}

[data-testid="metric-container"]{
    background-color:#f8f9fa;
    border:1px solid #eeeeee;
    padding:10px;
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CARGAR DATOS
# ══════════════════════════════════════════════════════════════

@st.cache_data
def cargar_datos():

    df = pd.read_csv('caso3_produccion_dataset.csv')

    df['fecha_produccion'] = pd.to_datetime(
        df['fecha_produccion']
    )

    return df

df = cargar_datos()

# ══════════════════════════════════════════════════════════════
# SIDEBAR — FILTROS
# ══════════════════════════════════════════════════════════════

with st.sidebar:

    st.header('⚙️ Filtros')

    turno_sel = st.multiselect(
        'Selecciona Turno',
        options=sorted(df['turno'].unique()),
        default=sorted(df['turno'].unique())
    )

    linea_sel = st.multiselect(
        'Selecciona Línea',
        options=sorted(df['linea_produccion'].unique()),
        default=sorted(df['linea_produccion'].unique())
    )

    maquina_sel = st.multiselect(
        'Selecciona Máquina',
        options=sorted(df['maquina'].unique()),
        default=sorted(df['maquina'].unique())
    )

# ══════════════════════════════════════════════════════════════
# APLICAR FILTROS SOLO PARA VISUALIZACIÓN
# (NO ES LIMPIEZA DE DATOS)
# ══════════════════════════════════════════════════════════════

df_filtrado = df[
    (df['turno'].isin(turno_sel)) &
    (df['linea_produccion'].isin(linea_sel)) &
    (df['maquina'].isin(maquina_sel))
]

# ══════════════════════════════════════════════════════════════
# TÍTULO PRINCIPAL
# ══════════════════════════════════════════════════════════════

st.title('🏭 Dashboard de Producción Industrial')

st.markdown("""
### Monitoreo de eficiencia, defectos y desempeño operativo
""")

st.markdown("""
#### 👨‍💻 Desarrollado por:
**Maria Paula Benavides** y **Nicolás Clavijo Hernández**
""")

st.markdown('---')

# ══════════════════════════════════════════════════════════════
# KPIs GENERALES
# ══════════════════════════════════════════════════════════════

eficiencia = df_filtrado['eficiencia_pct'].mean()

defectos = df_filtrado['tasa_defectos_pct'].mean()

unidades = df_filtrado['unidades_producidas'].sum()

costo = df_filtrado['costo_produccion_cop'].sum()

paro = df_filtrado['tiempo_paro_min'].sum()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    '⚙️ Eficiencia',
    f'{eficiencia:.2f}%'
)

k2.metric(
    '❌ Defectos',
    f'{defectos:.2f}%'
)

k3.metric(
    '📦 Producción',
    f'{unidades:,.0f}'
)

k4.metric(
    '💰 Costos',
    f'${costo:,.0f}'
)

k5.metric(
    '⏱️ Paros',
    f'{paro:,.0f} min'
)

st.markdown('---')

# ══════════════════════════════════════════════════════════════
# FILA 1
# ══════════════════════════════════════════════════════════════

col1, col2 = st.columns([1.5, 1])

# ══════════════════════════════════════════════════════════════
# GRÁFICA 1 — EFICIENCIA POR LÍNEA
# ══════════════════════════════════════════════════════════════

with col1:

    eficiencia_linea = (
        df_filtrado.groupby('linea_produccion')
        .agg(
            eficiencia_promedio=('eficiencia_pct', 'mean')
        )
        .reset_index()
    )

    fig1 = px.bar(
        eficiencia_linea,
        x='linea_produccion',
        y='eficiencia_promedio',
        color='eficiencia_promedio',
        color_continuous_scale='Pinkyl',
        text_auto='.2f',
        title='⚙️ Eficiencia Promedio por Línea'
    )

    fig1.update_layout(
        template='plotly_white'
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════
# GRÁFICA 2 — DEFECTOS POR TURNO
# ══════════════════════════════════════════════════════════════

with col2:

    defectos_turno = (
        df_filtrado.groupby('turno')
        .agg(
            defectos=('unidades_defectuosas', 'sum')
        )
        .reset_index()
    )

    fig2 = px.pie(
        defectos_turno,
        names='turno',
        values='defectos',
        title='❌ Defectos por Turno',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig2.update_layout(
        template='plotly_white'
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════
# FILA 2
# ══════════════════════════════════════════════════════════════

col3, col4 = st.columns([1, 1.5])

# ══════════════════════════════════════════════════════════════
# GRÁFICA 3 — PAROS POR MÁQUINA
# ══════════════════════════════════════════════════════════════

with col3:

    paros_maquina = (
        df_filtrado.groupby('maquina')
        .agg(
            tiempo_paro=('tiempo_paro_min', 'sum')
        )
        .reset_index()
        .sort_values('tiempo_paro')
    )

    fig3 = px.bar(
        paros_maquina,
        x='tiempo_paro',
        y='maquina',
        orientation='h',
        color='tiempo_paro',
        color_continuous_scale='Pinkyl',
        text_auto=True,
        title='🛑 Tiempo de Paro por Máquina'
    )

    fig3.update_layout(
        template='plotly_white'
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════
# GRÁFICA 4 — TEMPERATURA VS DEFECTOS
# ══════════════════════════════════════════════════════════════

with col4:

    fig4 = px.scatter(
        df_filtrado,
        x='temperatura_c',
        y='tasa_defectos_pct',
        color='linea_produccion',
        size='unidades_defectuosas',
        hover_data=[
            'maquina',
            'producto',
            'turno'
        ],
        title='🌡️ Temperatura vs Tasa de Defectos',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig4.update_layout(
        template='plotly_white'
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ══════════════════════════════════════════════════════════════
# GRÁFICA 5 — PRODUCCIÓN SEMANAL
# ══════════════════════════════════════════════════════════════

produccion_semana = (
    df_filtrado.groupby('semana')
    .agg(
        unidades=('unidades_producidas', 'sum')
    )
    .reset_index()
)

fig5 = px.line(
    produccion_semana,
    x='semana',
    y='unidades',
    markers=True,
    title='📈 Evolución Semanal de Producción',
    color_discrete_sequence=['#d81b60']
)

fig5.update_traces(
    line_width=4,
    marker_size=8
)

fig5.update_layout(
    template='plotly_white'
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ══════════════════════════════════════════════════════════════
# INSIGHTS FINALES
# ══════════════════════════════════════════════════════════════

st.markdown('---')

st.subheader('💡 Insights Relevantes')

st.markdown("""
- 🌙 El turno de noche presenta la mayor cantidad de unidades defectuosas.

- 🛑 La máquina **Torno-02** registra el mayor tiempo acumulado de paro.

- 📈 Algunas semanas muestran aumentos importantes en producción.

- 🌡️ Se evidencia relación entre temperaturas elevadas y mayores tasas de defectos.

### ✅ Recomendación Gerencial

Se recomienda intervenir prioritariamente el turno nocturno y realizar mantenimiento preventivo al Torno-02 para mejorar la eficiencia general y disminuir defectos.
""")

# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════

st.markdown('---')

st.caption(
    'Dashboard desarrollado por Maria Paula Benavides & Nicolás Clavijo Hernández'
)