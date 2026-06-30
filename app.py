import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Diseño: Título con estilo
st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓")
st.markdown("<h1 style='text-align: center; color: #004a99;'>🎓 Registro de Estudiantes - CECyTEH</h1>", unsafe_allow_html=True)

def conectar_gsheets():
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key("1O_SXAlng9f6GKmv566Jw-A2dbJwFiFFZcObin4S1g-c")
    return sh.sheet1

# Formulario con mejor diseño
with st.form("registro_form"):
    st.write("### Datos del Estudiante")
    # Usamos .upper() para forzar mayúsculas en el input
    nombre = st.text_input("Nombre del Alumno").upper()
    
    # Lista corregida de carreras
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
    
    st.write("---")
    violento = st.slider("Nivel de Violentómetro", 0, 10, 5)
    
    submit = st.form_submit_button("Guardar Registro")

    if submit:
        try:
            hoja = conectar_gsheets()
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Los datos ya van en mayúsculas gracias al .upper()
            datos = [fecha, nombre, carrera, semestre, grupo, tutor, observaciones, violento]
            hoja.append_row(datos)
            st.success("✅ ¡Registro guardado exitosamente!")
        except Exception as e:
            st.error(f"Error técnico: {e}")
