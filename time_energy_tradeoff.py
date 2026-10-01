import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =======================
# Load datasets
# =======================
path_1gb = '3D_relation_TPCH_1GB/3D_relation_tpch_1gb.csv'
path_3gb = '3D_relation_TPCH_3GB/3D_relation_tpch_3gb.csv'
path_5gb = '3D_relation_TPCH_5GB/3D_relation_tpch_5gb.csv'

df_1gb = pd.read_csv(path_1gb)
df_3gb = pd.read_csv(path_3gb)
df_5gb = pd.read_csv(path_5gb)

# =======================
# Clean data columns
# =======================
for df in [df_1gb, df_3gb, df_5gb]:
    for col in ['Execution_Time', 'total_energy_consumption_memory_plus_cpu']:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(',', '', regex=True).astype(float)
    if 'Total_Energy' not in df.columns and 'total_energy_consumption_memory_plus_cpu' in df.columns:
        df['Total_Energy'] = df['total_energy_consumption_memory_plus_cpu']

# =======================
# Setup figure layout (ACM full-width: 7 inches)
# =======================
queries = [f"Q{i}" for i in range(1, 23)]
x = np.arange(len(queries))
width = 0.28

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 4.8), sharex=True)

# =======================
# Panel (a): Execution Time
# =======================
ax1.bar(x - width, df_1gb['Execution_Time'], width, label='1 GB', color='#1f77b4', edgecolor='k', linewidth=0.4, zorder=3)
ax1.bar(x, df_3gb['Execution_Time'], width, label='3 GB', color='#ff7f0e', edgecolor='k', linewidth=0.4, zorder=3)
ax1.bar(x + width, df_5gb['Execution_Time'], width, label='5 GB', color='#2ca02c', edgecolor='k', linewidth=0.4, zorder=3)

ax1.set_ylabel('Execution Time (s)', fontsize=9, fontweight='normal')
ax1.set_title('(a) Query Execution Time Across Scale Factors', fontsize=11, fontweight='normal', loc='left')
ax1.legend(frameon=False, ncol=3, loc='upper left', fontsize=7)
ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

# =======================
# Panel (b): Total Energy
# =======================
ax2.bar(x - width, df_1gb['Total_Energy'], width, label='1 GB', color='#1f77b4', edgecolor='k', linewidth=0.4, zorder=3)
ax2.bar(x, df_3gb['Total_Energy'], width, label='3 GB', color='#ff7f0e', edgecolor='k', linewidth=0.4, zorder=3)
ax2.bar(x + width, df_5gb['Total_Energy'], width, label='5 GB', color='#2ca02c', edgecolor='k', linewidth=0.4, zorder=3)

ax2.set_ylabel('Total Energy (J)', fontsize=9, fontweight='normal')
ax2.set_title('(b) Total Energy Consumption Across Scale Factors', fontsize=11, fontweight='normal', loc='left')
ax2.set_xticks(x)
ax2.set_xticklabels(queries, fontsize=8, fontweight='normal', rotation=45, ha='right')
ax2.set_xlabel('TPC-H Query', fontsize=9, fontweight='normal')
ax2.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

# =======================
# Save outputs with safe padding for rotated labels
# =======================
plt.tight_layout()
output_path_png = '3D_relation_TPCH/tpch_execution_and_energy_comparison.png'
output_path_pdf = output_path_png.replace('.png', '.pdf')

plt.savefig(output_path_png, dpi=300, bbox_inches='tight', pad_inches=0.3)
plt.savefig(output_path_pdf, bbox_inches='tight', pad_inches=0.3)

plt.show()