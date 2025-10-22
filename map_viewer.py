import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd # / GeoPandas
st.set_page_config(layout="wide")
st.title("Leafmap ")

with st.sidebar:
    st.header("這是側邊攔")
    option = st.selectbox(
"選擇底圖:",
("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter")
)
    

url="https://maps.nlsc.gov.tw/download/鄉鎮市區界線(TWD97經緯度).zip"
gdf = gpd.read_file(url)    

st.write(f"你選擇的底圖是: {option}")

m = leafmap.Map(center=[24.0, 121.0], zoom=7) 
m.add_gdf(gdf, layer_name="Countries",style={"fillColor": "yellow", "color": "blue", "weight": 2, "fillOpacity": 0.1})



m.add_basemap("OpenTopoMap")
m.add_basemap("Esri.WorldImagery")
m.add_basemap("CartoDB.DarkMatter")

m.add_layer_control()
m.to_streamlit(height=700)
