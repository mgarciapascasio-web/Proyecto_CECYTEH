import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓", layout="wide")

# Estilo profesional
st.markdown("<h1 style='text-align: center; color: #004a99;'>🎓 Sistema CECyTEH</h1>", unsafe_allow_html=True)

# Función de conexión
def conectar_gsheets():
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key("1O_SXAlng9f6GKmv566Jw-A2dbJwFiFFZcObin4S1g-c")
    return sh.sheet1

# Crear pestañas
tab1, tab2 = st.tabs(["📝 Registrar Incidencia", "📊 Ver Registros"])

# --- PESTAÑA 1: REGISTRO ---
with tab1:
    with st.form("registro_form", clear_on_submit=True):
        st.write("### Captura de Datos")
        nombre = st.text_input("Nombre del Alumno").upper()
        
        carrera = st.selectbox("Carrera", [
            "Preparación de Alimentos y Bebidas", 
            "Procesos de Gestión Administrativa", 
            "Soporte y Gestión de Tecnologías Informáticas", 
            "Enfermería General"
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            semestre = st.selectbox("Semestre", ["1", "2", "3", "4", "5", "6"])
        with col2:
            grupo = st.text_input("Grupo").upper()
            
        tutor = st.text_input("Nombre del Tutor").upper()
        observaciones = st.text_area("Observaciones")
        violento = st.slider("Nivel de Violentómetro", 0, 10, 5)
        
        submit = st.form_submit_button("Guardar Registro")

        if submit:
            try:
                hoja = conectar_gsheets()
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                datos = [fecha, nombre, carrera, semestre, grupo, tutor, observaciones, violento]
                hoja.append_row(datos)
                
                # Alertas visuales según el nivel
                if violento >= 8:
                    st.error(f"⚠️ ¡ALERTA! Nivel crítico ({violento}) registrado.")
                elif violento >= 5:
                    st.warning(f"⚠️ Precaución: Nivel {violento} detectado.")
                else:
                    st.success("✅ ¡Registro guardado exitosamente!")
                
                # Recargar para limpiar campos
                st.rerun()
            except Exception as e:
                st.error(f"Error técnico: {e}")

# --- PESTAÑA 2: CONSULTA ---
with tab2:
    st.subheader("📋 Historial de Registros")
    if st.button("Actualizar tabla"):
        try:
            hoja = conectar_gsheets()
            rows = hoja.get_all_values()
            if len(rows) > 1:
                df = pd.DataFrame(rows[1:], columns=rows[0])
                st.dataframe(df, use_container_width=True)
            else:
                st.info("La tabla está vacía.")
        except Exception as e:
            st.warning("No se pudieron cargar los registros. Verifica tu conexión.")
