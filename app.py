import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓")

def conectar_gsheets():
    # Obtener el diccionario de credenciales
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # Asegurar que el salto de línea en la clave privada sea correcto
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    # Definir los alcances (scopes) necesarios para acceder a Sheets y Drive
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(creds)
    
    # Abrir la hoja por nombre
    sh = gc.open("Registro_CECYTEH_Metztitlán")
    return sh.sheet1

st.title("🎓 Registro CECyTEH")

with st.form("registro"):
    nombre = st.text_input("Nombre del Alumno")
    carrera = st.text_input("Carrera")
    tutor = st.text_input("Nombre del Tutor")
    observaciones = st.text_area("Observaciones")
    violento = st.slider("Nivel de Violentómetro", 0, 10, 0)
    submit = st.form_submit_button("Guardar Registro")

    if submit:
        try:
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            hoja = conectar_gsheets()
            hoja.append_row([fecha, nombre, carrera, tutor, observaciones, violento])
            st.success("¡Registro guardado exitosamente!")
        except Exception as e:
            st.error(f"Error detallado: {str(e)}")
