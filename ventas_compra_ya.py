import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import os

st.set_page_config(page_title="Ventas Compra Ya", layout="wide")
st.title("🛍️ VENTAS COMPRA YA")

# Archivos CSV
DATA_FILE = "ventas_data.csv"
CALENDAR_FILE = "calendario_mensual.csv"

# Horarios y vendedores
horas = [f"{h:02}:00" for h in range(6, 24)]
vendedores = ["Britany", "Victor", "Jeniffer"]

# Cargar datos
def cargar_datos():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, index_col=0)
    else:
        df = pd.DataFrame(0, index=horas, columns=vendedores)
        return df

def guardar_datos(df):
    df.to_csv(DATA_FILE)

def cargar_calendario():
    if os.path.exists(CALENDAR_FILE):
        return pd.read_csv(CALENDAR_FILE, index_col=0, parse_dates=True)
    else:
        hoy = date.today()
        dias_mes = pd.date_range(hoy.replace(day=1), periods=31, freq="D")
        dias_mes = dias_mes[dias_mes.month == hoy.month]
        calendario = pd.DataFrame(index=[d.date() for d in dias_mes], columns=["Ventas Totales"])
        calendario["Ventas Totales"] = 0
        return calendario

def guardar_calendario(df):
    df.to_csv(CALENDAR_FILE)

ventas = cargar_datos()
calendario = cargar_calendario()

# Ingreso de ventas por hora
st.subheader("🕒 Ingresar Ventas por Hora")
for hora in horas:
    cols = st.columns(len(vendedores) + 1)
    cols[0].markdown(f"**{hora}**")
    for i, vendedor in enumerate(vendedores):
        value = cols[i + 1].number_input(f"{hora} - {vendedor}", min_value=0, step=1, key=f"{hora}_{vendedor}", value=int(ventas.loc[hora, vendedor]))
        ventas.loc[hora, vendedor] = value

# Totales
st.subheader("📊 Totales por Hora y Totales del Día")
ventas["Total Hora"] = ventas.sum(axis=1)
total_dia = ventas["Total Hora"].sum()
st.dataframe(ventas.style.format(precision=0))
st.markdown(f"### 🔢 Total de Ventas del Día: **{int(total_dia)}**")

# Botón de guardar
if st.button("💾 Guardar ventas de hoy"):
    hoy = date.today()
    calendario.loc[hoy, "Ventas Totales"] = int(total_dia)
    guardar_calendario(calendario)
    guardar_datos(ventas)
    st.success("✅ Ventas guardadas correctamente.")

# Botón de reset
if st.button("🔁 Resetear ventas del día"):
    ventas.iloc[:, :-1] = 0
    guardar_datos(ventas)
    st.experimental_rerun()

# Calendario editable
st.subheader("📅 Registro Diario de Ventas - Calendario del Mes")
fecha_edit = st.date_input("Selecciona el día para editar:", date.today())
nuevo_valor = st.number_input("Nuevo valor de ventas:", min_value=0, step=1)
if st.button("Actualizar día seleccionado"):
    calendario.loc[fecha_edit, "Ventas Totales"] = nuevo_valor
    guardar_calendario(calendario)
    st.success(f"✅ Actualizado {fecha_edit} con Q{nuevo_valor}")

st.dataframe(calendario)

# Total acumulado
st.markdown(f"### 📈 Total Acumulado del Mes: **{int(calendario['Ventas Totales'].sum())}**")

# Gráfico de barras diario
st.subheader("📊 Gráfico Diario de Ventas por Vendedor")
fig1, ax1 = plt.subplots()
ventas[vendedores].sum().plot(kind="bar", ax=ax1, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
ax1.set_ylabel("Ventas del Día")
st.pyplot(fig1)

# Gráfico de barras mensual
st.subheader("📅 Gráfico Mensual Acumulado")
mensual_vendedores = {v: 0 for v in vendedores}
for dia in calendario.index:
    if isinstance(dia, str):
        dia = pd.to_datetime(dia).date()
    for v in vendedores:
        if os.path.exists(DATA_FILE):
            df_tmp = pd.read_csv(DATA_FILE, index_col=0)
            mensual_vendedores[v] += df_tmp[v].sum()

fig2, ax2 = plt.subplots()
pd.Series(mensual_vendedores).plot(kind="bar", ax=ax2, color=["#1f77b4", "#ff7f0e", "#2ca02c"])
ax2.set_ylabel("Ventas del Mes")
st.pyplot(fig2)
