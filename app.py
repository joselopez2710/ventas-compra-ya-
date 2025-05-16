
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Ventas Compra Ya", layout="wide")
st.title("📊 VENTAS COMPRA YA")

DATA_FILE = "ventas_data.csv"
CALENDAR_FILE = "calendario_mensual.csv"

# Cargar datos
def cargar_datos():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        horarios = [f"{h:02}:00" for h in range(6, 24)]
        df = pd.DataFrame(horarios, columns=["Hora"])
            df[vendedor] = 0
    return df

def guardar_datos(df):
    df.to_csv(DATA_FILE, index=False)

# Cargar calendario
def cargar_calendario():
    if os.path.exists(CALENDAR_FILE):
        return pd.read_csv(CALENDAR_FILE, index_col=0)
    else:
        hoy = datetime.now()
        dias = pd.date_range(f"{hoy.year}-{hoy.month:02}-01", periods=31, freq="D")
        dias = dias[dias.month == hoy.month]
        return pd.DataFrame(index=[f"{d.day:02}" for d in dias], columns=["Total"]).fillna("")

def guardar_calendario(df):
    df.to_csv(CALENDAR_FILE)

# Procesar
df = cargar_datos()
calendario = cargar_calendario()

# Formulario de entradas
st.subheader("🕓 Registro por Hora")
edited_df = st.data_editor(df, num_rows="dynamic")
if st.button("💾 Guardar Ventas del Día"):
    guardar_datos(edited_df)
    st.success("✅ Ventas guardadas")
    df = edited_df

# Totales
df_numeric = df.drop("Hora", axis=1)
df["Total por Hora"] = df_numeric.sum(axis=1)
total_dia = df_numeric.sum().sum()
st.subheader("📈 Totales")
st.metric("💰 Total del Día", f"Q{total_dia:.2f}")

# Actualizar calendario
hoy = datetime.now().day
dia_str = f"{hoy:02}"
if st.button("📆 Registrar en Calendario"):
    calendario.loc[dia_str, "Total"] = total_dia
    guardar_calendario(calendario)
    st.success("✅ Día actualizado en calendario")

# Mostrar calendario y editar
st.subheader("📅 Calendario Mensual")
calendario_edit = st.data_editor(calendario)
if st.button("💾 Guardar Calendario"):
    guardar_calendario(calendario_edit)
    st.success("✅ Cambios en el calendario guardados")

# Botón de reset
if st.button("🔄 Reiniciar Ventas del Día"):
        df[vendedor] = 0
    guardar_datos(df)
    st.experimental_rerun()
