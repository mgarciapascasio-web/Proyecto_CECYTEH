import streamlit as st
import gspread
from datetime import datetime

# Conexión con Google Sheets
gc = gspread.service_account(filename='credenciales.json')
sh = gc.open("Registro_CECYTEH_Metztitlan")
hoja = sh.sheet1

st.title("🎓 Registro CECyTEH - Metztitlán")

# Lista de carreras oficiales
carreras_lista = [
    "Preparación de Alimentos y Bebidas", 
    "Procesos de Gestión Administrativa", 
    "Soporte y Gestión de Tecnologías Informáticas", 
    "Enfermería General"
]

# Formulario
with st.form("registro_form"):
    nombre = st.text_input("Nombre del alumno")
    carrera = st.selectbox("Carrera", carreras_lista)
    semestre = st.selectbox("Semestre", ["1", "2", "3", "4", "5", "6"])
    grupo = st.text_input("Grupo")
    tutor = st.text_input("Nombre del Tutor")
    observaciones = st.text_area("Observaciones")
    violentometro = st.slider("Nivel de Violentómetro", 0, 10, 0)
    
    submit = st.form_submit_button("Guardar Registro")

if submit:
    try:
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        # El orden coincide con: Fecha, Nombre, Carrera, Semestre, Grupo, Tutor, Observaciones, Violentómetro
        hoja.append_row([fecha, nombre, carrera, semestre, grupo, tutor, observaciones, violentometro])
        st.success("¡Registro guardado exitosamente!")
    except Exception as e:
        st.error(f"Error al guardar: {e}")