import streamlit as st
import gspread

# Page config
st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓")

# Connection to Google Sheets
def conectar_gsheets():
    creds_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(creds_dict)
    sh = gc.open("Registro_CECYTEH_Metztitlán")
    return sh.sheet1

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
                st.error(f"Error: {e}")
        else:
            st.warning("Por favor, llena todos los campos.")