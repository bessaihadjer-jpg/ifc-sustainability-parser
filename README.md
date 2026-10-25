\# 🏗️ IFC Sustainability Metric Extractor



\[!\[Streamlit App](https://static.streamlit.io/badges/streamlit\_badge\_black\_white.svg)](https://your-app-url.streamlit.app)



A lightweight, browser-based BIM tool built with Python and Streamlit. This application parses Industry Foundation Classes (IFC) files to automatically extract early-stage sustainability metrics and visualize spatial data.



\*\*Live Demo:\*\* \[Try the application here](https://ifc-sustainability-parser-8qyzj7472jdutaked38wvp.streamlit.app/)



\## ✨ Features

\* \*\*Automated Data Extraction\*\*: Reads `IfcWall` and `IfcWindow` BaseQuantities to calculate total areas.

\* \*\*Sustainability Metrics\*\*: Instantly computes the Window-to-Wall Ratio (WWR) for early-stage energy performance analysis.

\* \*\*Semantic 3D Visualization\*\*: Extracts X, Y, Z coordinates to generate an interactive 3D point cloud of the building elements using Plotly.

\* \*\*Live Demo Capability\*\*: Integrates `requests` to fetch open-source IFC models directly from GitHub for one-click testing.



\## 🛠️ Tech Stack

\* \*\*Language\*\*: Python 3

\* \*\*BIM Parsing\*\*: `IfcOpenShell`

\* \*\*Data Processing\*\*: `pandas`

\* \*\*Visualization\*\*: `plotly`

\* \*\*Web UI\*\*: `streamlit`



\## 🚀 How to Run Locally

1\. Clone the repository: `git clone https://github.com/YourUsername/ifc-sustainability-parser.git`

2\. Install dependencies: `pip install -r requirements.txt`

3\. Launch the app: `streamlit run app.py`



\*Developed as part of a computational design and AI-BIM research portfolio.\*

