import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

# Configuración inicial
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

# Pestañas
tab1, tab2 = st.tabs(["📝 Registrar Incidencia", "📊 Ver Registros"])

with tab1:
    with st.form("registro_form", clear_on_submit=True):
        st.write("### ✍️ Captura de Nueva Incidencia")
        
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
        observaciones = st.text_area("Observaciones", height=150)
        violento = st.slider("Nivel de Violentómetro", 0, 10, 0)
        
        submit = st.form_submit_button("Guardar Registro")

        if submit:
            if not matricula or not nombre or not grupo or not tutor:
                st.error("⚠️ Error: Todos los campos son obligatorios.")
            else:
                try:
                    hoja = conectar_gsheets()
                    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    hoja.append_row([fecha, matricula, nombre, carrera, semestre, grupo, tutor, observaciones, violento])
                    
                    if violento >= 8:
                        st.toast("¡Alerta! Caso crítico registrado", icon="🚨")
                        st.error(f"⚠️ ¡Nivel crítico ({violento}) detectado!")
                    elif violento >= 5:
                        st.toast("Registro guardado con precaución", icon="⚠️")
                        st.warning(f"⚠️ Precaución: Nivel {violento} detectado.")
                    else:
                        st.toast("¡Registro guardado con éxito!", icon="✅")
                        st.success("✅ ¡Información registrada correctamente!")
                except Exception as e:
                    st.error("❌ Error al guardar en base de datos.")
                    with st.expander("Detalles técnicos"): st.write(e)

with tab2:
    st.subheader("📋 Historial de Registros")
    
    if st.button("🔄 Cargar/Actualizar tabla"):
        try:
            hoja = conectar_gsheets()
            rows = hoja.get_all_values()
            st.session_state.df = pd.DataFrame(rows[1:], columns=rows[0])
            st.session_state.data_loaded = True
        except:
            st.error("Error al conectar con Google Sheets.")

    if 'data_loaded' in st.session_state:
        busqueda = st.text_input("🔍 Buscar por Matrícula...", key="input_busqueda")
        
        df_mostrar = st.session_state.df
        if busqueda:
            mask = st.session_state.df['Matrícula'].str.contains(busqueda.strip().upper(), case=False, na=False)
            df_mostrar = st.session_state.df[mask]
        
        # MEJORA: Colorear filas según nivel de violencia
        def colorear_violencia(row):
            val = int(row['Nivel de Violentómetro'])
            if val >= 8: return ['background-color: #ffcccc'] * len(row)
            if val >= 5: return ['background-color: #fff3cc'] * len(row)
            return [''] * len(row)
        
        styled_df = df_mostrar.style.apply(colorear_violencia, axis=1)
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        csv = df_mostrar.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar tabla a CSV", csv, "reporte_cecyteh.csv", "text/csv")
