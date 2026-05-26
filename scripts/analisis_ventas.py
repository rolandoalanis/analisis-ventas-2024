# =============================================================
# Análisis de Ventas 2024 - Organización Empresarial - UTN TUP
# Escenario B: Análisis de Ventas de una Pequeña Empresa
# =============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. CARGA DE DATOS
URL = "https://gist.githubusercontent.com/khanusama20/ee33c2869dd5cf3cebdf020be1ca43f6/raw/cbcbbb2651dd0b631d7bd194bc51b2fbb105d108/sales_sample_2024.csv"
df = pd.read_csv(URL)
df['sales_date'] = pd.to_datetime(df['sales_date'])
os.makedirs('datos', exist_ok=True)
df.to_csv('datos/sales_sample_2024.csv', index=False)
print("Dataset guardado en /datos")

# 2. INDICADORES GENERALES
ventas_totales = df['sales_amount'].sum()
venta_promedio = df['sales_amount'].mean()
venta_maxima   = df['sales_amount'].max()
venta_minima   = df['sales_amount'].min()
dia_max = df.loc[df['sales_amount'].idxmax(), 'sales_date'].strftime('%d/%m/%Y')
dia_min = df.loc[df['sales_amount'].idxmin(), 'sales_date'].strftime('%d/%m/%Y')

print("\n===== INDICADORES GENERALES =====")
print(f"Ventas totales:      $ {ventas_totales:,.0f}")
print(f"Promedio diario:     $ {venta_promedio:,.0f}")
print(f"Día mayor venta:     {dia_max}  ($ {venta_maxima:,})")
print(f"Día menor venta:     {dia_min}  ($ {venta_minima:,})")

# 3. VENTAS POR MES
df['mes'] = df['sales_date'].dt.to_period('M')
ventas_mes = df.groupby('mes')['sales_amount'].sum().reset_index()
ventas_mes.columns = ['Mes', 'Total']
print("\n===== VENTAS POR MES =====")
print(ventas_mes.to_string(index=False))

# 4. GRÁFICO
os.makedirs('resultados', exist_ok=True)
meses = [str(m) for m in ventas_mes['Mes']]
totales = ventas_mes['Total'].values
fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(meses, totales, color='steelblue', edgecolor='white')
bars[ventas_mes['Total'].idxmax()].set_color('seagreen')
bars[ventas_mes['Total'].idxmin()].set_color('tomato')
ax.set_title('Evolución Mensual de Ventas - 2024', fontsize=14, fontweight='bold')
ax.set_xlabel('Mes')
ax.set_ylabel('Total Ventas ($)')
ax.tick_params(axis='x', rotation=45)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
for bar, val in zip(bars, totales):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300,
            f'${val:,.0f}', ha='center', va='bottom', fontsize=7)
plt.tight_layout()
plt.savefig('resultados/ventas_mensuales_2024.png', dpi=150)
plt.show()
print("\nGráfico guardado en /resultados")
