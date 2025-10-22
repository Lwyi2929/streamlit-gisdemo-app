import streamlit as st
import pandas as pd
st.title("Streamlit 核心  Widgets")
# 1. 把 Widgets 放到側邊攔 (sidebar)
with st.sidebar:st.header("這是側邊攔")
# 選擇框 (Selectbox)
option = st.selectbox(
"你最喜歡的 GIS 軟體?",
("QGIS", "ArcGIS", "ENVI", "GRASS")
)
# 滑桿 (Slider)
year = st.slider("選擇一個年份", 1990, 2030, 2024)
# 2. 在主頁顯示 Widgets 的結果
st.write(f"你選擇的軟體是: {option}")
st.write(f"你選擇的年份是: {year}")
# 按鈕 (Button)
if st.button("點我顯示氣球!"):
st.balloons()
# 檔案上傳 (File Uploader) 地理系必備!
uploaded_file = st.file_uploader(
"上傳你的 Shapefile (.zip) 或 GeoTIFF (.tif) 或 GeoJSON (.json)",
type=["zip", "tif", "json"]
)
if uploaded_file is not None:
st.success(f"你上傳了: {uploaded_file.name} (大小: {uploaded_file.size} bytes)")