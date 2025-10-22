import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd 

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

# 使用 st.cache_data 緩存資料，避免每次運行都重新下載和解析 Shapefile
@st.cache_data(show_spinner="正在下載並解析地理資料...")
def load_data(url):
    """使用 GeoPandas 讀取遠端壓縮檔中的 Shapefile。"""
    return gpd.read_file(url)

try:
    gdf = load_data(url) 
    
except Exception as e:
    # 顯示錯誤訊息並停止應用程式
    st.error(f"讀取地理資料失敗，請檢查網路連線或資料來源。錯誤訊息: {e}")
    st.stop()


# --- 資料檢查與概覽 (新增) ---
st.subheader("地理資料概覽")
if gdf.empty:
    st.warning("GeoDataFrame 載入成功，但內容為空。地圖將無法顯示邊界。")
    st.stop()
else:
    # 顯示前五筆資料，確認欄位名稱和內容
    st.write(f"成功載入 {len(gdf)} 筆資料，欄位如下：")
    st.dataframe(gdf[['COUNTYNAME', 'TOWNNAME', 'geometry']].head())
    

st.markdown(f"**目前選擇的底圖:** `{selected_option}`")

# --- 初始化 Leafmap 地圖 ---
# 關鍵修改: 使用 selected_option 作為初始底圖 (tiles 參數)
m = leafmap.Map(
    center=[23.7, 120.95], # 調整中心點以更好地顯示台灣
    zoom=8,
    tiles=selected_option # <--- 這是設定初始底圖的關鍵
) 

# --- 添加 GeoDataFrame 圖層 ---
# 添加台灣鄉鎮市區界線
m.add_gdf(
    gdf,
    layer_name="台灣鄉鎮市區界線",
    style={
        "fillColor": "#4d9221", # 填充色 (綠色系)
        "color": "#ffffff",     # 邊線顏色改為白色，在深色底圖上更顯眼
        "weight": 1.5,          # 邊線粗細
        "fillOpacity": 0.05,    # 填充透明度
        "opacity": 1.0          # 邊線透明度提高到 1.0
    },
    tooltip=["COUNTYNAME", "TOWNNAME"] # 滑鼠懸停時顯示縣市和鄉鎮名稱
)

# 將其他可選底圖添加到地圖控制元件中，以便用戶可以在地圖上切換
for tile in base_map_options:
    if tile != selected_option:
        m.add_basemap(tile)

# 添加圖層控制按鈕 (可以切換 GeoDataFrame 圖層和底圖)
m.add_layer_control()

# 在 Streamlit 中顯示地圖
m.to_streamlit(height=700)