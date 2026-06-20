# Asteroid Core Intelligence Platform ☄️📊

An interactive orbital analytics platform and data intelligence system designed to ingest, process, and map near-Earth objects (NEOs). The system synchronizes deep analytical data exploration with programmatic telemetry viewports to cross-examine planetary close approach risks.

---

## 🚀 System Architecture & Overview

This platform implements an end-to-end data product, bridging advanced cloud data engineering with high-performance client-side visualization. The system is split into three main operational layers:


```

[ Raw Kaggle Data Ingestion ] ──> [ Microsoft Fabric Pipelines ] ──> [ Optimized Parquet/CSV Delta ]
│
▼
[ Three.js 3D Telemetry HUD ] <── [ Reactive Cross-Filtering ] <─── [ Streamlit Analytical Engine ]

```

1. **Ingestion & Data Engineering:** Scalable data lakehouse pipeline optimized for large-scale astronomical time-series processing.
2. **Analytical Engine:** Dynamic interactive UI featuring synchronized real-time cross-filtering between metric distributions, distribution matrices, and physical object tables.
3. **Telemetry Engine:** Interactive WebGL component rendering real-time orbital trajectories, flight vectors, and proximity telemetry directly within the intelligence viewports.

---

## 🛠️ Tech Stack

### 💾 Data Pipeline & Storage
* **Microsoft Fabric:** Orchestration of data engineering workflows via automated Lakehouse pipelines.
* **Apache Spark / Delta Lake:** Automated raw data cleansing, schema enforcement, data type parsing (ISO datetime structures), and calculation of operational states (`is_future`).

### ⚙️ Backend & Analytical UI
* **Python 3.11+ & Streamlit:** Core state management, dynamic sidebar controls, reactive widgets, and structural layouts via modular tab views (`st.tabs`).
* **Pandas:** High-speed, in-memory analytical vector operations and synchronized client-side data frame slicing.
* **Plotly Express & Graph Objects:** High-frequency rendering of multi-variable scatter matrices, responsive doughnut charts, and contextual risk metrics mapped to strict astronomical thresholds (e.g., PHA boundaries).

### 🌌 3D Simulation Engine
* **Three.js (WebGL):** Client-side hardware-accelerated 3D rendering pipeline for dynamic celestial bodies and orbital paths.
* **OrbitControls:** Fluid interactive target tracking, responsive camera panning, and geometric perspective zooming.
* **Custom Telemetry HUD:** Dynamic HTML5/CSS3 UI overlays providing spatial orientation markers and vector-based velocity feeds.

---

## 🔬 Core Analytical Capabilities

* **NASA PHA Classification Rules:** Built-in validation algorithms mapping objects against strict criteria: Absolute Magnitude ($H \le 22.0$) and Minimum Orbit Intersection Distance ($\text{MOID} \le 0.05 \text{ au}$ / $\le 19.5 \text{ LD}$).
* **Dynamic Chronological Slicing:** Continuous temporal detection split point identifying historical data blocks vs. real-time predictive future alerts based on structural clock timestamps.
* **Symmetric Cross-Filtering:** Bidirectional data isolation where graphical element clicks (Plotly selection states) automatically propagate downstream to re-index, slice, and scale summary tables and performance metrics instantly.

```