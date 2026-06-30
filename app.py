import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="Sistema Integral CECyTEH", page_icon="🎓", layout="wide")

# Estilos CSS para los KPIs
st.markdown("""
    <style>
    div[data-testid="metric-container"] { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #004a99; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #004a99;'>🎓 Sistema Integral CECyTEH</h1>", unsafe_allow_html=True)

def conectar_gsheets():
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(creds)
    return gc.open_by_key("1O_SXAlng9f6GKmv566Jw-A2dbJwFiFFZcObin4S1g-c").sheet1

tab1, tab2 = st.tabs(["📝 Registrar Incidencia", "📊 Panel de Control"])

with tab1:
    with st.form("registro_form", clear_on_submit=True):
        st.write("### ✍️ Captura de Nueva Incidencia")
        col1, col2 = st.columns(2)
        with col1: matricula = st.text_input("Matrícula").strip().upper()
        with col2: nombre = st.text_input("Nombre del Alumno").strip().upper()
        
        carrera = st.selectbox("Carrera", ["Preparación de Alimentos y Bebidas", "Procesos de Gestión Administrativa", "Soporte y Gestión de Tecnologías Informáticas", "Enfermería General"])
        
        c3, c4 = st.columns(2)
        with c3: semestre = st.selectbox("Semestre", ["1", "2", "3", "4", "5", "6"])
        with c4: grupo = st.text_input("Grupo").strip().upper()
            
        tutor = st.text_input("Nombre del Tutor").strip().upper()
        observaciones = st.text_area("Observaciones", height=120)
        violento = st.slider("Nivel de Violentómetro", 0, 10, 0)
        
        if st.form_submit_button("Guardar Registro"):
            if not matricula or not nombre or not grupo or not tutor:
                st.error("⚠️ Error: Campos obligatorios vacíos.")
            else:
                with st.spinner('Guardando en base de datos...'):
                    try:
                        hoja = conectar_gsheets()
                        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        hoja.append_row([fecha, matricula, nombre, carrera, semestre, grupo, tutor, observaciones, violento])
                        
                        # Notificaciones según riesgo
                        if violento >= 8: st.error(f"⚠️ Alerta: Nivel crítico ({violento}) registrado.")
                        else: st.success("✅ ¡Incidencia guardada con éxito!")
                    except: st.error("❌ Error de conexión con Google Sheets.")

with tab2:
    st.subheader("📊 Panel de Control y Métricas")
    if st.button("🔄 Actualizar Datos"):
        with st.spinner('Cargando registros...'):
            try:
                hoja = conectar_gsheets()
                data = hoja.get_all_values()
                st.session_state.df = pd.DataFrame(data[1:], columns=data[0])
                st.session_state.data_loaded = True
            except: st.error("Error de conexión.")

    if 'data_loaded' in st.session_state:
        df = st.session_state.df
        df['Nivel de Violentómetro'] = pd.to_numeric(df['Nivel de Violentómetro'])
        
        # --- KPIs ---
        k1, k2, k3 = st.columns(3)
        k1.metric("Total Registros", len(df))
        k2.metric("Casos Críticos (8+)", len(df[df['Nivel de Violentómetro'] >= 8]))
        k3.metric("Promedio de Riesgo", round(df['Nivel de Violentómetro'].mean(), 1))

        st.markdown("---")
        
        # --- FILTROS INTELIGENTES ---
        f1, f2 = st.columns([1, 2])
        with f1:
            niveles = st.multiselect("Filtrar por nivel de riesgo:", [0,1,2,3,4,5,6,7,8,9,10], default=list(range(11)))
        with f2:
            busqueda = st.text_input("🔍 Buscar por Matrícula...").strip().upper()
            
        # Filtrado lógico
        df_mostrar = df[df['Nivel de Violentómetro'].isin(niveles)]
        if busqueda:
            df_mostrar = df_mostrar[df_mostrar['Matrícula'].str.contains(busqueda, case=False, na=False)]
        
        # Estilo de colores
        def highlight_row(row):
            val = int(row['Nivel de Violentómetro'])
            if val >= 8: return ['background-color: #ffcccc'] * len(row)
            if val >= 5: return ['background-color: #fff3cc'] * len(row)
            return [''] * len(row)

        st.dataframe(df_mostrar.style.apply(highlight_row, axis=1), use_container_width=True, hide_index=True)
        st.download_button("📥 Descargar Reporte Completo", df.to_csv(index=False).encode('utf-8'), "reporte_cecyteh.csv")
