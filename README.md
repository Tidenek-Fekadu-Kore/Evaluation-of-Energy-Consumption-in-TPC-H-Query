Energy Consumption and Performance Evaluation in TPC-H Query Processing

Overview:
This repository contains the experimental artifact, workload configurations, raw measurement datasets, and plotting utilities used to evaluate the relationship between execution time, CPU energy, memory energy, and total energy consumption across TPC-H query workloads at multiple data volumes (1 GB, 3 GB, and 5 GB).

Methodology & Attribution:
The energy estimation and profiling framework applied in this study builds upon the real-time energy estimation methodology established by Kore et al. (2025):
Kore Tidenek Fekadu, Sarramia David, Kang Myoung-Ah, and Pinet François.
2025. Towards sustainable DBMS: A framework for real-time energy estima-
tion and query categorization. In Proc. 29th Int. Symp. on Database Engineered
Applications (IDEAS 2025). 171–183. doi:10.1007/978-3-032-06744-9_1.


Repository Structure

```text
├── 3D_relation_TPCH_1GB/
│   ├── 3D_relation_tpch_1gb.csv
│   ├── updated_tpch_1gb_with_power...
│   ├── query_3d_plot_1gb_tpch.pdf
│   └── query_3d_plot_1gb_tpch.png
├── 3D_relation_TPCH_3GB/
│   ├── 3D_relation_tpch_3gb.csv
│   ├── updated_tpch_3gb_with_power...
│   ├── query_3d_plot_3gb_tpch.pdf
│   └── query_3d_plot_3gb_tpch.png
├── 3D_relation_TPCH_5GB/
│   ├── 3D_relation_tpch_5gb.csv
│   ├── updated_tpch_5gb_with_power...
│   ├── query_3d_plot_5gb_tpch.pdf
│   └── query_3d_plot_5gb_tpch.png
├── workload_TPCH/
│   ├── tpch_queries.sql
├── 3D_relation_with_legend.py
└── time_energy_tradeoff.py

Component Description

workload_TPCH/:

tpch_queries.sql: Contains the standard 22 TPC-H SQL queries adapted for evaluation.


3D_relation_TPCH_*GB/:

CSV measurement logs (.csv) captured execution time, CPU energy, memory energy, and total energy metrics for Scale Factors 1 GB, 3 GB, and 5 GB.

Contains  3D plots visualizing the multi-dimensional energy-performance trade-offs.
Python Utilities (.py):

3D_relation_with_legend.py: Generates the standardized 3D visual relationships.
time_energy_tradeoff.py: Processes the performance versus energy consumption data across query structures and data volumes.

Reproduction Instructions

Environment Setup: Ensure your target database engine and hardware performance monitoring interface (supporting the energy estimation framework) are fully configured.

Execute Workload: Run the TPC-H query workload using the orchestration tools provided in workload_TPCH/.

Generate Visualizations: Execute the plotting scripts from the root directory to recreate the evaluation figures and data summaries:
    
Bash

python3 3D_relation_with_legend.py
python3 time_energy_tradeoff.py
