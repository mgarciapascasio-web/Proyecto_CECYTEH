import streamlit as st
import gspread

# 1. Configuración de la página
st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓")

# 2. Conexión segura a Google Sheets
def conectar_gsheets():
    # Usamos los datos guardados en la sección 'Secrets' de Streamlit
    creds_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(creds_dict)
    
    # IMPORTANTE: Asegúrate de que este nombre sea EXACTAMENTE el de tu archivo en Google Drive
    sh = gc.open("Registro_CECYTEH_Metztitlán") 
    return sh.sheet1

# 3. Interfaz de usuario
st.title("🎓 Registro de Estudiantes - CECyTEH")
st.write("Completa los datos para el registro:")

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
                st.error(f"Error de conexión: {e}")
        else:
            st.warning("Por favor, llena todos los campos.")
