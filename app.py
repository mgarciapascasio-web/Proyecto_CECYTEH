import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuración básica
st.set_page_config(page_title="Registro", page_icon="🎓")

def conectar_gsheets():
    # Cargar y reparar la clave privada
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    # Autorizar
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(creds)
    
    # Conexión directa al ID
    sh = gc.open_by_key("1O_SXAlng9f6GKmv566Jw-A2dbJwFiFFZcObin4S1g-c")
    return sh.sheet1 # Accede a la primera hoja directamente

st.title("🎓 Registro de Estudiantes")

with st.form("registro_form"):
    nombre = st.text_input("Nombre")
    carrera = st.selectbox("Carrera", ["Alimentos", "Administración", "Informática", "Enfermería"])
    semestre = st.selectbox("Semestre", ["1", "2", "3", "4", "5", "6"])
    grupo = st.text_input("Grupo")
    tutor = st.text_input("Nombre del Tutor")
    observaciones = st.text_area("Observaciones")
    violento = st.slider("Violentómetro", 0, 10, 5)
    submit = st.form_submit_button("Guardar Registro")

    if submit:
        try:
            # Conectar
            hoja = conectar_gsheets()
            # Escribir
            datos = [str(datetime.now()), nombre, carrera, semestre, grupo, tutor, observaciones, violento]
            hoja.append_row(datos)
            st.success("✅ ¡Guardado!")
        except Exception as e:
            st.error(f"Error: {e}")
