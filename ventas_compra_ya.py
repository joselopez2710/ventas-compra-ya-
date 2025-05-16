
import streamlit as st 
import pandas as pd
from datetime import datetime, date
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ventas Compra Ya", layout="wide")
st.title("🛍️ VENTAS COMPRA YA")

# Definir horarios y vendedores
horas = [f"{h:02}:00" for h in range(6, 24)]
vendedores = ["Britany", "Victor", "Jeniffer"]
hoy = date.today()
DATA_FILE = "ventas_data.csv"
CALENDARIO_FILE = "calendario_data.csv"

# Inicializar DataFrame de ventas
if os.path.exists(DATA_FILE):
    ventas = pd.read_csv(DATA_FILE, index_col=0)
else:
    ventas = pd.DataFrame(0, index=horas, columns=vendedores)

st.subheader("🕒 Ingresar Ventas por Hora")
for hora in horas:
    cols = st.columns(len(vendedores) + 1)
    cols[0].markdown(f"**{hora}**")
    for i, vendedor in enumerate(vendedores):
        value = cols[i + 1].number_input(f"{hora} - {vendedor}", min_value=0, step=1, value=int(ventas.loc[hora, vendedor]), key=f"{hora}_{vendedor}")
        ventas.loc[hora, vendedor] = value

# Mostrar tabla de ventas por hora
ventas["Total Hora"] = ventas.sum(axis=1)
total_dia = int(ventas["Total Hora"].sum())

st.subheader("📊 Totales por Hora")
st.dataframe(ventas.style.format(precision=0))
st.markdown(f"### 🔢 Total de Ventas del Día: **{total_dia}**")

# Mostrar gráfico de ventas por vendedor del día
st.subheader("📈 Gráfico Diario de Ventas")
totales_vendedor = ventas[vendedores].sum()
fig, ax = plt.subplots()
totales_vendedor.plot(kind="bar", ax=ax)
ax.set_ylabel("Ventas")
ax.set_title("Ventas Totales por Vendedor (Hoy)")
st.pyplot(fig)

# Cargar calendario mensual
dias_mes = pd.date_range(hoy.replace(day=1), periods=31, freq="D")
dias_mes = dias_mes[dias_mes.month == hoy.month]

if os.path.exists(CALENDARIO_FILE):
    calendario = pd.read_csv(CALENDARIO_FILE, index_col=0)
    calendario.index = pd.to_datetime(calendario.index).date
else:
    calendario = pd.DataFrame(index=[d.date() for d in dias_mes], columns=vendedores)
    calendario = calendario.fillna(0)

# Botón para guardar ventas de hoy en el calendario
if st.button("💾 Guardar ventas de hoy"):
    for vendedor in vendedores:
        calendario.loc[hoy, vendedor] = int(ventas[vendedor].sum())
    calendario.to_csv(CALENDARIO_FILE)
    ventas[vendedores].to_csv(DATA_FILE)
    st.success("✅ Ventas guardadas correctamente.")

# Botón para resetear las ventas del día
if st.button("🔁 Resetear ventas del día"):
    ventas[vendedores] = 0
    ventas.to_csv(DATA_FILE)
    st.rerun()

# Mostrar calendario
st.subheader("📅 Calendario del Mes")
st.dataframe(calendario)

# Mostrar totales del mes por vendedor
st.subheader("📈 Total Acumulado del Mes por Vendedor")
totales_mes = calendario.sum()
for vendedor in vendedores:
    st.markdown(f"- **{vendedor}**: {int(totales_mes[vendedor])}")

# Gráfico mensual
st.subheader("📊 Gráfico de Ventas Mensuales")
fig2, ax2 = plt.subplots()
totales_mes.plot(kind="bar", ax=ax2)
ax2.set_ylabel("Ventas")
ax2.set_title("Total de Ventas por Vendedor (Mes)")
st.pyplot(fig2)
