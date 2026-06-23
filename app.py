import streamlit as st
import gspread

# Configuración de la página
st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓")

# Conexión a Google Sheets
def conectar_gsheets():
    # Usamos las credenciales de los Secrets
    creds_dict = dict(st.secrets["gcp_service_account"])
    # Reparamos el formato de la llave privada
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
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
                # Aquí es donde se envían los datos a la hoja
                sheet.append_row([nombre, matricula])
                st.success(f"¡Registro exitoso de {nombre}!")
            except Exception as e:
                st.error(f"Error técnico: {e}")
        else:
            st.warning("Por favor, llena todos los campos.")