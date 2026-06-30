import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# Configuración
st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓", layout="wide")

# Cabecera con espacio para logo (opcional) y título
col1, col2 = st.columns([1, 6])
with col1:
    st.write("### 🏫") # Aquí podrías poner st.image("tu_logo.png")
with col2:
    st.markdown("<h1 style='color: #004a99;'>Sistema CECyTEH</h1>", unsafe_allow_html=True)

def conectar_gsheets():
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key("1O_SXAlng9f6GKmv566Jw-A2dbJwFiFFZcObin4S1g-c")
    return sh.sheet1

tab1, tab2 = st.tabs(["📝 Registrar Incidencia", "📊 Ver Registros"])

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
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            semestre = st.selectbox("Semestre", ["1", "2", "3", "4", "5", "6"])
        with col_c2:
            grupo = st.text_input("Grupo").upper()
            
        tutor = st.text_input("Nombre del Tutor").upper()
        observaciones = st.text_area("Observaciones", height=150)
        violento = st.slider("Nivel de Violentómetro", 0, 10, 5)
        
        submit = st.form_submit_button("Guardar Registro")

        if submit:
            if not nombre or not grupo or not tutor:
                st.error("⚠️ Error: Por favor, llena todos los campos obligatorios.")
            else:
                try:
                    hoja = conectar_gsheets()
                    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    datos = [fecha, nombre, carrera, semestre, grupo, tutor, observaciones, violento]
                    hoja.append_row(datos)
                    
                    if violento >= 8:
                        st.toast("¡Alerta! Caso crítico registrado", icon="🚨")
                        st.error(f"⚠️ ¡Nivel crítico ({violento}) detectado!")
                    else:
                        st.toast("¡Registro guardado con éxito!", icon="✅")
                        st.success("✅ ¡Información registrada correctamente!")
                except Exception as e:
                    st.error("❌ Error de conexión.")
                    with st.expander("Detalles"): st.write(e)

with tab2:
    st.subheader("📋 Historial de Registros")
    if st.button("🔄 Actualizar tabla"):
        try:
            hoja = conectar_gsheets()
            rows = hoja.get_all_values()
            if len(rows) > 1:
                df = pd.DataFrame(rows[1:], columns=rows[0])
                
                # BUSCADOR
                busqueda = st.text_input("🔍 Buscar por nombre de alumno...")
                if busqueda:
                    df = df[df['Nombre del Alumno'].str.contains(busqueda, case=False, na=False)]
                
                st.dataframe(df, use_container_width=True)
                
                # BOTÓN DE DESCARGA
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Descargar tabla a Excel (CSV)",
                    data=csv,
                    file_name='reporte_cecyteh.csv',
                    mime='text/csv',
                )
            else:
                st.info("La tabla está vacía.")
        except Exception as e:
            st.warning("No se pudieron cargar los registros.")
