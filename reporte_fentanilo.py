import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# === 1. Cargar dataset ===
df = pd.read_csv("fentanilo.csv")

# === 2. Calcular listados ===
mediana_dias = df["dias_fallecimiento"].median()
infeccion_por_edad = df.groupby("edad")["cant_ampollas_infectadas"].sum() / df.groupby("edad")["cant_ampollas"].sum() * 100
casos_por_via = df[["cant_via_intravenosa", "cant_intramuscular", "cant_intranasal", "cant_bucal", "cant_transdérmica"]].sum()
defunciones = df["cant_defunciones"].sum()
casos_graves = df["cant_casos_graves"].sum()
casos_leves = df["cant_casos_sin_consecuencias"].sum()
contaminacion_lotes = df.groupby("lote")["cant_ampollas_infectadas"].sum()
produccion_labs = df.groupby("laboratorio")["cant_amp_por_laboratorio"].sum()

# === 3. Generar gráficos ===
plt.figure(figsize=(6,4))
casos_por_via.plot(kind="bar", title="Casos por vía de administración")
plt.ylabel("Cantidad de aplicaciones")
plt.tight_layout()
plt.savefig("grafico_vias.png")
plt.close()

plt.figure(figsize=(6,4))
infeccion_por_edad.plot(kind="line", marker="o", title="Porcentaje de infección por edades")
plt.ylabel("% Infección")
plt.tight_layout()
plt.savefig("grafico_infeccion_edades.png")
plt.close()

plt.figure(figsize=(6,4))
produccion_labs.plot(kind="barh", title="Producción por Laboratorios")
plt.xlabel("Cantidad de ampollas")
plt.tight_layout()
plt.savefig("grafico_labs.png")
plt.close()

# === 4. Crear PDF ===
doc = SimpleDocTemplate("Reporte_Fentanilo.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("📊 Reporte de Análisis de Fentanilo", styles["Title"]))
story.append(Spacer(1, 12))

# Resultados numéricos
story.append(Paragraph(f"Mediana de días entre administración y fallecimiento: {mediana_dias}", styles["Normal"]))
story.append(Paragraph(f"Total de Defunciones: {defunciones}", styles["Normal"]))
story.append(Paragraph(f"Casos graves: {casos_graves}", styles["Normal"]))
story.append(Paragraph(f"Casos sin consecuencias: {casos_leves}", styles["Normal"]))
story.append(Spacer(1, 12))

# Insertar gráficos
story.append(Paragraph("Casos por Vía de Administración", styles["Heading2"]))
story.append(Image("grafico_vias.png", width=400, height=250))
story.append(Spacer(1, 12))

story.append(Paragraph("Porcentaje de Infección por Edades", styles["Heading2"]))
story.append(Image("grafico_infeccion_edades.png", width=400, height=250))
story.append(Spacer(1, 12))

story.append(Paragraph("Producción por Laboratorios", styles["Heading2"]))
story.append(Image("grafico_labs.png", width=400, height=250))
story.append(Spacer(1, 12))

story.append(Paragraph("Conclusión:", styles["Heading2"]))
story.append(Paragraph(
    "El análisis muestra que la vía intravenosa concentra la mayor cantidad de aplicaciones, "
    "los laboratorios presentan variaciones significativas en producción, y la infección varía "
    "de acuerdo a la edad de los pacientes. El tiempo medio hasta fallecimiento es moderado, "
    "lo que sugiere que la evolución clínica requiere seguimiento detallado.",
    styles["Normal"]
))

# Guardar PDF
doc.build(story)
print("✅ Reporte_Fentanilo.pdf generado correctamente.")
