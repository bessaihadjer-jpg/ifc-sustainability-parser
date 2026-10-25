import streamlit as st
import ifcopenshell
import os
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IFC Sustainability Parser", layout="wide")

# --- HELPER FUNCTIONS ---
def get_element_area(element):
    """Extracts area from IFC BaseQuantities."""
    for rel in getattr(element, 'IsDefinedBy', []):
        if rel.is_a("IfcRelDefinesByProperties"):
            prop_set = rel.RelatingPropertyDefinition
            if prop_set.is_a("IfcElementQuantity"):
                for quantity in prop_set.Quantities:
                    if quantity.is_a("IfcQuantityArea") and "Area" in quantity.Name:
                        return float(quantity.AreaValue)
    return 0.0

def get_element_location(element):
    """Extracts X, Y, Z coordinates from an IFC element's placement."""
    try:
        coords = element.ObjectPlacement.RelativePlacement.Location.Coordinates
        return coords[0], coords[1], coords[2]
    except Exception:
        return None, None, None
# -----------------------

st.title("🏗️ IFC Sustainability Metric Extractor")
st.markdown("Upload an Industry Foundation Classes (IFC) file or use our live sample to extract spatial data.")

col_upload, col_sample = st.columns(2)

with col_upload:
    uploaded_file = st.file_uploader("Upload an IFC file", type=['ifc'])

with col_sample:
    st.info("No IFC file handy? Use a real open-source BIM model.")
    use_sample = st.button("Load Online Sample Model")

temp_path = "temp_model.ifc"
file_ready = False

if uploaded_file is not None:
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    file_ready = True
elif use_sample:
    with st.spinner("Downloading sample model from GitHub..."):
        sample_url = "https://raw.githubusercontent.com/viktor-platform/ifc-sample-models/main/sample-models/BuildingBIMModel.ifc"
        response = requests.get(sample_url)
        with open(temp_path, "wb") as f:
            f.write(response.content)
        file_ready = True

if file_ready:
    with st.spinner("Parsing IFC geometry and quantities..."):
        ifc_model = ifcopenshell.open(temp_path)
        
        st.subheader("Model Metadata")
        col1, col2 = st.columns(2)
        col1.metric("IFC Schema", ifc_model.schema)
        col2.metric("Total Elements", len(ifc_model.by_type("IfcProduct")))
        
        st.subheader("Early-Stage Sustainability Metrics")
        
        walls = ifc_model.by_type("IfcWall") + ifc_model.by_type("IfcWallStandardCase")
        windows = ifc_model.by_type("IfcWindow")
        
        total_wall_area = sum([get_element_area(wall) for wall in walls])
        total_window_area = sum([get_element_area(window) for window in windows])
        wwr = (total_window_area / total_wall_area * 100) if total_wall_area > 0 else 0.0
            
        col3, col4, col5 = st.columns(3)
        col3.metric("Total Wall Area", f"{total_wall_area:.2f} m²")
        col4.metric("Total Window Area", f"{total_window_area:.2f} m²")
        col5.metric("Window-to-Wall Ratio", f"{wwr:.1f} %")
        
        # --- 3D DATA VISUALIZATION ---
        st.subheader("Spatial Distribution (3D Point Cloud)")
        
        data = []
        for wall in walls:
            x, y, z = get_element_location(wall)
            if x is not None:
                data.append({"Element": "Wall", "X": x, "Y": y, "Z": z})
                
        for window in windows:
            x, y, z = get_element_location(window)
            if x is not None:
                data.append({"Element": "Window", "X": x, "Y": y, "Z": z})
                
        if data:
            df = pd.DataFrame(data)
            fig = px.scatter_3d(df, x='X', y='Y', z='Z', color='Element', 
                                title="Building Elements in 3D Space",
                                color_discrete_map={"Wall": "#808080", "Window": "#87CEEB"})
            fig.update_traces(marker=dict(size=4))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Could not extract spatial coordinates from this specific IFC file.")
        
    os.remove(temp_path)