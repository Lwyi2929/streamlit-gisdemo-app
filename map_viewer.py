# ...existing code...
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import tempfile
import urllib.request
import os

# 設置 Streamlit 頁面為寬版佈局
st.set_page_config(layout="wide")
st.title("台灣鄉鎮市區界線地圖 (Leafmap)")

# --- 側邊欄設定 ---
with st.sidebar:
    st.header("地圖設定")

    # 可選底圖列表
    base_map_options = ["OpenTopoMap", "Esri.WorldImagery", "CartoDB.DarkMatter", "Stadia.StamenToner"]

    # 讓用戶選擇底圖，將選擇結果存入 selected_option
    selected_option = st.selectbox(
        "選擇底圖:",
        base_map_options
    )
    st.markdown("---")
    st.info("地圖顯示的邊界資料來自國家地理空間資訊服務網站。")

# --- 讀取地理資料 (台灣鄉鎮市區界線) ---
url = "https://maps.nlsc.gov.tw/download/鄉鎮市區界線(TWD97經緯度).zip"

@st.cache_data
def load_data_from_zip_url(url):
    """
    嘗試直接用 geopandas 讀取遠端 zip；若失敗則下載到暫存檔再讀取。
    """
    try:
        # 先嘗試直接讀取（某些環境可行）
        return gpd.read_file(url)
    except Exception:
        # 失敗 -> 下載到暫存檔再讀取
        tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
        tmp.close()
        try:
            urllib.request.urlretrieve(url, tmp.name)
            gdf = gpd.read_file(tmp.name)
            return gdf
        finally:
            try:
                os.remove(tmp.name)
            except Exception:
                pass

# 讀取資料並處理錯誤
try:
    gdf = load_data_from_zip_url(url)
except Exception as e:
    st.error(f"載入地理資料失敗：{e}")
    st.stop()

# --- 資料檢查與概覽 ---
st.subheader("地理資料概覽")
if gdf is None or gdf.empty:
    st.warning("GeoDataFrame 載入成功，但內容為空或無法解析。地圖將無法顯示邊界。")
    st.stop()
else:
    st.write(f"成功載入 {len(gdf)} 筆資料，欄位如下：")
    # 若欄位不存在，避免 key error
    cols = [c for c in ["COUNTYNAME", "TOWNNAME", "geometry"] if c in gdf.columns]
    st.dataframe(gdf[cols].head())

st.markdown(f"**目前選擇的底圖:** `{selected_option}`")

# --- 初始化 Leafmap 地圖 ---
m = leafmap.Map(
    center=[23.7, 120.95],
    zoom=8,
    tiles=selected_option
)

# --- 添加 GeoDataFrame 圖層 ---
m.add_gdf(
    gdf,
    layer_name="台灣鄉鎮市區界線",
    style={
        "fillColor": "#4d9221",
        "color": "#ffffff",
        "weight": 1.5,
        "fillOpacity": 0.05,
        "opacity": 1.0
    },
    tooltip=[col for col in ["COUNTYNAME", "TOWNNAME"] if col in gdf.columns]
)

for tile in base_map_options:
    if tile != selected_option:
        m.add_basemap(tile)

m.add_layer_control()
m.to_streamlit(height=700)
# ...existing code...