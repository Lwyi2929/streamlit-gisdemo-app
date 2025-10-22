import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# Set page config before any Streamlit output
st.set_page_config(layout="wide")

with st.sidebar:
    st.header("側邊攔")

    option = st.selectbox(
    "請選擇底圖",
    ("OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter"),
)

st.title("Leafmap + GeoPandas:台南市媽祖廟宇分布圖")

url="Tainan_temple_mazhou.zip"
gdf=gpd.read_file(url)
st.dataframe(gdf.head())

# 建立地圖
m = leafmap.Map(center=[23.0, 120.2], zoom=12)
m.add_basemap(option)

# 將 GeoDataFrame 加入地圖（修正 style 鍵名）
m.add_gdf(
    gdf,
    layer_name="台南市媽祖廟宇分布圖",
    style={"fillOpacity": 0, "color": "black", "weight": 0.5},
    highlight=False,
)

m.add_layer_control()

# 顯示地圖
m.to_streamlit(height=700)