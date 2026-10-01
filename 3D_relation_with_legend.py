import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

# =======================
# Load data one at time
# =======================
#file_path = '3D_relation_TPCH_5GB/3D_relation_tpch_1gb.csv'
#file_path = '3D_relation_TPCH_5GB/3D_relation_tpch_3gb.csv'
file_path = '3D_relation_TPCH_5GB/3D_relation_tpch_5gb.csv'

df = pd.read_csv(file_path)

# =======================
# Clean string numbers (Removes commas)
# =======================
for col in ['Input_Rows', 'Output_Rows', 'Execution_Time', 'Energy_Consumed_CPU']:
    if col in df.columns and df[col].dtype == 'object':
        df[col] = df[col].astype(str).str.replace(',', '', regex=True).astype(float)

# =======================
# Preprocess & Power Calculation
# =======================
df = df[df['Execution_Time'] > 0]
df['Total_Energy'] = df['total_energy_consumption_memory_plus_cpu']
df['Power_Consumption'] = df['Total_Energy'] / df['Execution_Time']

# 1. Define the mapping from query numbers to short category names
category_mapping = {
    1: 'Agg & Group',
    2: 'Join + Subquery',
    3: 'Multi-Join + Group',
    4: 'Exists + Group',
    5: 'Multi-Join + Group',
    6: 'Basic Scan',
    7: 'Derived Join + Group',
    8: 'Case Join + Group',
    9: 'Multi-Join + Group',
    10: 'Multi-Join + Group',
    11: 'Join + Subquery',
    12: 'Case Join + Group',
    13: 'Outer Join',
    14: 'Case Join + Division',
    15: 'View / Admin',
    16: 'Distinct Join + Subquery',
    17: 'Join + Subquery',
    18: 'Multi-Join + Group',
    19: 'Disjunctive Join',
    20: 'Nested Subquery Join',
    21: 'Exists Join + Group',
    22: 'Complex Subquery',
}

# 2. Ensure your 'Type' column is numeric
df['Type'] = pd.to_numeric(df['Type'])
df['Short_Type'] = df['Type'].map(category_mapping)

# 3. Create a label mapping that includes the Query IDs
type_to_queries = {}
for q_id, s_type in category_mapping.items():
    type_to_queries.setdefault(s_type, []).append(str(q_id))

legend_labels = {
    s_type: f"[Q{','.join(q_ids)}] {s_type}" 
    for s_type, q_ids in type_to_queries.items()
}
df['Legend_Label'] = df['Short_Type'].map(legend_labels)

# 4. Unique types
unique_types = df['Legend_Label'].unique()

# =======================
# Explicit High-Contrast Color Mapping
# =======================
color_dict = {
    '[Q1] Agg & Group': '#1f77b4',
    '[Q2,11,17] Join + Subquery': '#2ca02c',
    '[Q3,5,9,10,18] Multi-Join + Group': '#d62728',
    '[Q4] Exists + Group': '#000080',
    '[Q6] Basic Scan': '#ff7f0e',
    '[Q7] Derived Join + Group': '#8c564b',
    '[Q8,12] Case Join + Group': '#e377c2',
    '[Q13] Outer Join': '#7f7f7f',
    '[Q14] Case Join + Division': '#bcbd22',
    '[Q15] View / Admin': '#17becf',
    '[Q16] Distinct Join + Subquery': '#ff1493',
    '[Q19] Disjunctive Join': '#ffd700',
    '[Q20] Nested Subquery Join': '#00ffff',
    '[Q21] Exists Join + Group': '#adff2f',
    '[Q22] Complex Subquery': '#8510f3',
}

colors = df['Legend_Label'].map(color_dict)

# =======================
# Legend elements
# =======================
legend_elements = [
    Line2D([0], [0], marker='o', linestyle='None', label=qtype,
           markerfacecolor=color_dict.get(qtype, '#000000'), markeredgecolor='k',
           markeredgewidth=0, markersize=5)
    for qtype in unique_types
]

# =======================
# Create 3D plot (ACM-compliant dimensions)
# =======================
fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect(None, zoom=0.85)

# =======================
# Scatter plot
# =======================
ax.scatter(
    df['Input_Rows'],
    df['Output_Rows'],
    df['Power_Consumption'],
    c=colors,
    marker='o',
    s=30,
    edgecolor='k',
    linewidth=0,
    depthshade=False
)

# =======================
# Axis labels & Ticks (Optimized density)
# =======================
ax.set_xlabel('Total Accessed Rows', labelpad=8, fontsize=9, fontweight='normal')
ax.set_ylabel('Output Rows', labelpad=8, fontsize=9, fontweight='normal')
ax.set_zlabel('Power Consumption (W)', labelpad=12, fontsize=9, fontweight='normal')
ax.tick_params(axis='both', which='major', labelsize=8)

# Reduce tick density across all axes to prevent crowding
ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
ax.zaxis.set_major_locator(MaxNLocator(nbins=4))

# =======================
# Adjust viewing angle
# =======================
ax.view_init(elev=25, azim=-60)

# =======================
# Legend
# =======================
ax.legend(
    handles=legend_elements,
    title='TPC-H Queries Type',
    loc='upper center',
    bbox_to_anchor=(0.5, 1.32),
    ncol=2,
    fontsize=8,
    title_fontsize=9,
    frameon=False,
    columnspacing=0.8,
    handletextpad=0.3
)

# =======================
# Save updated CSV and Figures (PNG & PDF with padding)
# =======================
output_csv_path = '3D_relation_TPCH_5GB/updated_tpch_5gb_with_power.csv'
df.to_csv(output_csv_path, index=False)

plot_path_png = '3D_relation_TPCH_5GB/query_3d_plot_5gb_tpch.png'
plot_path_pdf = plot_path_png.replace('.png', '.pdf')

plt.savefig(plot_path_png, dpi=300, bbox_inches='tight', pad_inches=0.6)
plt.savefig(plot_path_pdf, bbox_inches='tight', pad_inches=0.6)

plt.show()