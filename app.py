import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuración
st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓")

def conectar_gsheets():
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(creds)
    # ID de tu hoja (el que confirmamos)
    sh = gc.open_by_key("1HS8LB5Y79KXvgaco_Ry420thbPNRKpOQObC6AhREMJQ")
    return sh.sheet1

st.title("🎓 Registro de Estudiantes - CECyTEH")

with st.form("registro_form"):
    nombre = st.text_input("Nombre del Alumno")
    
    # Menú desplegable con tus carreras
    carrera = st.selectbox("Carrera", [
        "Preparación de Alimentos y Bebidas",
        "Procesos de Gestión Administrativa",
        "Soporte y Gestión de Tecnologías Informáticas",
        "Enfermería General"
    ])
    
    semestre = st.selectbox("Semestre", ["1", "2", "3", "4", "5", "6"])
    grupo = st.text_input("Grupo")
    tutor = st.text_input("Nombre del Tutor")
    observaciones = st.text_area("Observaciones")
    violento = st.slider("Nivel de Violentómetro", 0, 10, 5)
    
    submit = st.form_submit_button("Guardar Registro")

    if submit:
        try:
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            hoja = conectar_gsheets()
            
            # Orden de las 8 columnas: [Fecha, Nombre, Carrera, Semestre, Grupo, Tutor, Obs, Violentómetro]
            datos = [fecha, nombre, carrera, semestre, grupo, tutor, observaciones, violento]
            
            hoja.append_row(datos)
            st.success("✅ ¡Registro guardado exitosamente!")
        except Exception as e:
            st.error(f"Error técnico (404): Asegúrate de que el ID de la hoja sea correcto. Detalle: {str(e)}")
