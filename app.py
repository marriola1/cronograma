import streamlit as st
import pandas as pd
from datetime import datetime, date

st.title("📅 Cronograma de Actividades por Cliente")

# Cargar datos iniciales
data = [
    {"Cliente": "Argos", "Actividad": "Enviar reporte", "Fecha Entrega": "2025-06-14", "Confirmado": False},
    {"Cliente": "BAC", "Actividad": "Aplicar pagos", "Fecha Entrega": "2025-06-12", "Confirmado": False},
    {"Cliente": "Cemaco", "Actividad": "Planilla mensual", "Fecha Entrega": "2025-06-10", "Confirmado": False},
]

df = pd.DataFrame(data)

# Mostrar tabla con botones
for i, row in df.iterrows():
    st.markdown(f"### Cliente: {row['Cliente']}")
    st.write(f"📝 Actividad: {row['Actividad']}")
    st.write(f"📆 Fecha programada: {row['Fecha Entrega']}")
    
    # Confirmar entrega
    confirm = st.checkbox("✅ Confirmar entrega", key=i)
    df.at[i, "Confirmado"] = confirm

    # Evaluar estado
    fecha_entrega = datetime.strptime(row["Fecha Entrega"], "%Y-%m-%d").date()
    hoy = date.today()

    if confirm and hoy == fecha_entrega:
        st.success("✔️ Entregado a tiempo")
    elif confirm and hoy > fecha_entrega:
        st.error("❌ Entregado tarde")
    elif not confirm and hoy > fecha_entrega:
        st.warning("⚠️ No se ha entregado")
    else:
        st.info("⏳ Pendiente")

    st.markdown("---")
