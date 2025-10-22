import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd 

# 設置 Streamlit 頁面為寬版佈局
st.set_page_config(layout="wide")
st.title("世界國家邊界地圖 (Leafmap)")

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
    st.info("地圖顯示的邊界資料來自 Natural Earth (1:110m)。")

# --- 讀取地理資料 (世界國家邊界) ---
# 使用 Natural Earth 1:110m 國家邊界資料
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"

# 使用 st.cache_data 緩存資料，避免每次運行都重新下載和解析 Shapefile
@st.cache_data(show_spinner="正在下載並解析世界國家邊界資料...")
def load_world_countries(url):
    """使用 GeoPandas 讀取遠端壓縮檔中的 Shapefile (世界國家邊界資料)。"""
    return gpd.read_file(url)

try:
    gdf = load_world_countries(url) 
    
except Exception as e:
    # 顯示錯誤訊息並停止應用程式
    st.error(f"讀取地理資料失敗，請檢查網路連線或資料來源。錯誤訊息: {e}")
    st.stop()


# --- 資料檢查與概覽 ---
st.subheader("世界國家邊界資料概覽")
if gdf.empty:
    st.warning("GeoDataFrame 載入成功，但內容為空。地圖將無法顯示邊界。")
    st.stop()
else:
    # 顯示前五筆資料，確認欄位名稱和內容 (使用 NAME 欄位)
    st.write(f"成功載入 {len(gdf)} 筆國家資料，部分欄位如下：")
    st.dataframe(gdf[['NAME', 'geometry']].head())
    

st.markdown(f"**目前選擇的底圖:** `{selected_option}`")

# --- 初始化 Leafmap 地圖 ---
# 調整中心點和縮放以顯示全球
m = leafmap.Map(
    center=[0, 0], # 全球中心點
    zoom=2,        # 較小的縮放級別以顯示全球
    tiles=selected_option # <--- 這是設定初始底圖的關鍵
) 

# --- 添加 GeoDataFrame 圖層 ---
# 添加世界國家邊界
m.add_gdf(
    gdf,
    layer_name="世界國家邊界",
    style={
        "fillColor": "#4d9221", # 填充色 (綠色系)
        "color": "#ffffff",     # 邊線顏色改為白色，在深色底圖上更顯眼
        "weight": 1.5,          # 邊線粗細
        "fillOpacity": 0.05,    # 填充透明度
        "opacity": 1.0          # 邊線透明度提高到 1.0
    },
    tooltip=["NAME"] # 滑鼠懸停時顯示國家名稱
)

# 將其他可選底圖添加到地圖控制元件中，以便用戶可以在地圖上切換
for tile in base_map_options:
    if tile != selected_option:
        m.add_basemap(tile)

# 添加圖層控制按鈕 (可以切換 GeoDataFrame 圖層和底圖)
m.add_layer_control()

# 在 Streamlit 中顯示地圖
m.to_streamlit(height=700)