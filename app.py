import streamlit as st
import gspread

# Configuración de la página
st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓")

# Conexión a Google Sheets
def conectar_gsheets():
    # Cargar credenciales desde los secretos de Streamlit
    creds = dict(st.secrets["gcp_service_account"])
    
    # REPARACIÓN DE FORMATO: Convierte los \n escritos en saltos de línea reales
    if "private_key" in creds:
        creds["private_key"] = creds["private_key"].replace("\\n", "\n")
    
    gc = gspread.service_account_from_dict(creds)
    sh = gc.open("Registro_CECYTEH_Metztitlán")
    return sh.sheet1

st.title("🎓 Registro de Estudiantes - CECyTEH")

with st.form("registro_form"):
    nombre = st.text_input("Nombre del Estudiante")
    matricula = st.text_input("Matrícula")
    submit = st.form_submit_button("Registrar")

    if submit:
        if nombre and matricula:
            try:
                sheet = conectar_gsheets()
                sheet.append_row([nombre, matricula])
                st.success(f"¡Registro exitoso de {nombre}!")
            except Exception as e:
                st.error(f"Error técnico: {e}")
        else:
            st.warning("Por favor, llena todos los campos.")