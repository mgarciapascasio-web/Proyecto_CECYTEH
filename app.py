import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Registro CECyTEH", page_icon="🎓", layout="wide")

st.markdown("<h1 style='text-align: center; color: #004a99;'>🎓 Sistema CECyTEH</h1>", unsafe_allow_html=True)
st.markdown("---")

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
        st.write("### ✍️ Captura de Nueva Incidencia")
        
        # Campo nuevo: Matrícula
        matricula = st.text_input("Matrícula del Alumno").strip().upper()
        nombre = st.text_input("Nombre del Alumno").strip().upper()
        
        carrera = st.selectbox("Carrera", [
            "Preparación de Alimentos y Bebidas", 
            "Procesos de Gestión Administrativa", 
            "Soporte y Gestión de Tecnologías Informáticas", 
            "Enfermería General"
        ])
        
        c1, c2 = st.columns(2)
        with c1: semestre = st.selectbox("Semestre", ["1", "2", "3", "4", "5", "6"])
        with c2: grupo = st.text_input("Grupo").strip().upper()
            
        tutor = st.text_input("Nombre del Tutor").strip().upper()
        observaciones = st.text_area("Observaciones", height=120)
        violento = st.slider("Nivel de Violentómetro", 0, 10, 0)
        
        submit = st.form_submit_button("Guardar Registro")

        if submit:
            if not matricula or not nombre:
                st.error("⚠️ Error: La Matrícula y el Nombre son obligatorios.")
            else:
                try:
                    hoja = conectar_gsheets()
                    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    datos = [fecha, matricula, nombre, carrera, semestre, grupo, tutor, observaciones, violento]
                    hoja.append_row(datos)
                    st.toast("¡Incidencia registrada!", icon="✅")
                    st.success("✅ Registro guardado exitosamente.")
                except Exception as e:
                    st.error("❌ Error al guardar.")

with tab2:
    st.subheader("📋 Historial de Registros")
    if st.button("🔄 Actualizar y Cargar Datos"):
        try:
            hoja = conectar_gsheets()
            rows = hoja.get_all_values()
            if len(rows) > 1:
                df = pd.DataFrame(rows[1:], columns=rows[0])
                
                # BUSCADOR POR MATRÍCULA
                busqueda = st.text_input("🔍 Buscar por Matrícula...").strip().upper()
                
                if busqueda:
                    mask = df['Matrícula'].str.contains(busqueda, case=False, na=False)
                    st.dataframe(df[mask], use_container_width=True)
                else:
                    st.dataframe(df, use_container_width=True)
                
                st.download_button("📥 Descargar reporte a CSV", df.to_csv(index=False).encode('utf-8'), "reporte.csv", "text/csv")
            else:
                st.info("La tabla está vacía.")
        except Exception as e:
            st.warning("No se pudieron cargar los datos.")
