import streamlit as st
import pandas as pd
from datetime import date

# Título de la app
st.title("📅 Cronograma de Actividades por Cliente")

# Cargar archivo Excel
excel_file = 'FORMATO DE CRONOGRAMA CONTA.xlsm'

# Leer las hojas disponibles
xls = pd.ExcelFile(excel_file)
sheet_names = xls.sheet_names

# Selector de mes (hoja)
selected_month = st.selectbox("Selecciona el mes", sheet_names)
df = pd.read_excel(xls, sheet_name=selected_month, header=1)

# Limpiar columnas
columnas_validas = [col for col in df.columns if isinstance(col, str) and "Cliente" in df.columns]
df = df.dropna(subset=['Cliente', 'Actividad'], how='all')

# Unificar columnas necesarias
columnas = {
    'Cliente': 'Cliente',
    'Actividad': 'Actividad',
    'Fecha Semana 1': 'Fecha Semana 1',
    'Confirmacion': 'Confirmacion',
    'Estado': 'Estado'
}

# Filtro por cliente
clientes = df['Cliente'].dropna().unique().tolist()
cliente_filtrado = st.selectbox("Filtrar por cliente", ["Todos"] + clientes)

if cliente_filtrado != "Todos":
    df = df[df['Cliente'] == cliente_filtrado]

# Mostrar tabla con resumen por semana
st.subheader("📋 Tareas")

total = 0
at_tiempo = 0
fuera_tiempo = 0
pendientes = 0

for index, row in df.iterrows():
    for semana in range(1, 6):
        fecha_col = f'Fecha Semana {semana}'
        conf_col = 'Confirmacion'

        if fecha_col in row and pd.notna(row[fecha_col]):
            total += 1
            fecha_entrega = pd.to_datetime(row[fecha_col]).date()
            hoy = date.today()
            confirmacion = bool(row.get(conf_col, False))

            st.markdown(f"### 🧾 {row['Cliente']} - {row['Actividad']}")
            st.write(f"📅 Fecha: {fecha_entrega}")

            if confirmacion and hoy == fecha_entrega:
                st.success("✔️ Entregado a tiempo")
                at_tiempo += 1
            elif confirmacion and hoy > fecha_entrega:
                st.error("❌ Entregado tarde")
                fuera_tiempo += 1
            elif not confirmacion and hoy > fecha_entrega:
                st.warning("⚠️ No se ha entregado")
                pendientes += 1
            else:
                st.info("⏳ Aún dentro de plazo")

            st.markdown("---")

# Resumen
st.subheader("📊 Resumen del mes")
st.write(f"🔢 Total de tareas: {total}")
st.write(f"✅ A tiempo: {at_tiempo}")
st.write(f"❌ Fuera de tiempo: {fuera_tiempo}")
st.write(f"⚠️ Pendientes vencidas: {pendientes}")

