import streamlit as st
import pandas as pd
st.title("關於我")

st.header("李玟儀的 GIS 專題")
st.write("")


# 1. ê Widgets t (sidebar)
with st.sidebar:
    st.header("ot")
#  (Selectbox)
    option = st.selectbox(
"oÝö GIS ?",
("QGIS", "ArcGIS", "ENVI", "GRASS")
)
# (Slider)
    year = st.slider("/[~:", 1990, 2030, 2024)

# 2. ¿¯ Widgets öÿ
st.write(f"oöo: {option}")
st.write(f"oö~o: {year}")
#  (Button)
if st.button("s!"):
    st.balloons()
# þNó (File Uploader) - vß!
    uploaded_file = st.file_uploader(
"Nóoö Shapefile (.zip) v GeoTIFF (.tif) v GeoJSON (.json)",
type=["zip", "tif", "json"]
)
if uploaded_file is not None:st.success(f"oNó: {uploaded_file.name} (//: {uploaded_file.size} bytes)")