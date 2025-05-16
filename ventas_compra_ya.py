
import streamlit as st 
import pandas as pd
from datetime import datetime, date
import os

st.set_page_config(page_title="Ventas Compra Ya", layout="wide")
st.title("🛍️ VENTAS COMPRA YA")

DATA_FILE = "ventas_guardadas.csv"
CALENDAR_FILE = "calendario_mensual.csv"

# Definir horarios de 6AM a 11PM
horas = [f"{h:02}:00" for h in range(6, 24)]
vendedores = ["Britany", "Victor", "Jeniffer"]

# Cargar datos previos si existen
def cargar_datos():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, index_col=0)
    else:
        return pd.DataFrame(0, index=horas, columns=vendedores)

def cargar_calendario():
    if os.path.exists(CALENDAR_FILE):
        cal = pd.read_csv(CALENDAR_FILE, index_col=0)
        cal.index = pd.to_datetime(cal.index).date
        return cal
    else:
        hoy = date.today()
        dias_mes = pd.date_range(hoy.replace(day=1), periods=31, freq="D")
        dias_mes = dias_mes[dias_mes.month == hoy.month]
        return pd.DataFrame(0, index=[d.date() for d in dias_mes], columns=["Ventas Totales"])

st.session_state.ventas = cargar_datos()
st.session_state.calendario = cargar_calendario()

# Botón para resetear ventas del día
if st.button("🔁 Resetear ventas del día"):
    st.session_state.ventas.loc[:, :] = 0
    st.success("Ventas diarias restablecidas.")

st.subheader("🕒 Ingresar Ventas por Hora")
for hora in horas:
    cols = st.columns(len(vendedores) + 1)
    cols[0].markdown(f"**{hora}**")
    for i, vendedor in enumerate(vendedores):
        value = cols[i + 1].number_input(f"{hora} - {vendedor}", min_value=0, step=1, value=int(st.session_state.ventas.loc[hora, vendedor]), key=f"{hora}_{vendedor}")
        st.session_state.ventas.loc[hora, vendedor] = value

# Total por hora y total del día
st.subheader("📊 Totales")
ventas = st.session_state.ventas.copy()
ventas["Total Hora"] = ventas.sum(axis=1)
total_dia = ventas["Total Hora"].sum()

st.dataframe(ventas.style.format(precision=0))
st.markdown(f"### 🔢 Total de Ventas del Día: **{int(total_dia)}**")

# Guardar los datos actualizados
st.session_state.ventas.to_csv(DATA_FILE)

# Calendario mensual
st.subheader("📅 Registro Diario de Ventas - Calendario del Mes")
hoy = date.today()

# Registro diario editable
if st.button("Guardar ventas de hoy"):
    st.session_state.calendario.loc[hoy, "Ventas Totales"] = int(total_dia)
    st.session_state.calendario.to_csv(CALENDAR_FILE)
    st.success("Ventas del día guardadas en el calendario.")

# Permitir edición manual del calendario
st.markdown("#### ✏️ Editar valores del calendario")
for i, row in st.session_state.calendario.iterrows():
    nuevo_valor = st.number_input(f"{i}", value=int(row["Ventas Totales"]), key=f"edit_{i}")
    st.session_state.calendario.loc[i, "Ventas Totales"] = nuevo_valor

st.session_state.calendario.to_csv(CALENDAR_FILE)
st.dataframe(st.session_state.calendario)

st.markdown(f"### 📈 Total Acumulado del Mes: **{st.session_state.calendario['Ventas Totales'].sum()}**")
