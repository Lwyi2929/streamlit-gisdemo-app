import streamlit as st
# 1. 使用 st.Page() 定義所有頁面
# 注意:st.Page() 會自動尋找.py 的檔案
# Emoji Wÿhttps://tw.piliapp.com/emoji/list/
pages = [
st.Page("page_home.py", title="專案首頁", icon="🌲"),
st.Page("page_map.py", title="互動地圖瀏覽", icon="🌎"),
st.Page("page_about.py", title="關於我們", icon="🩷")
]
# 2. 使用 st.navigation() 建立導覽 (例如在側邊攔)
with st.sidebar:
st.title("App 導覽")
# st.navigation() Þóö¿¯
selected_page = st.navigation(pages)
# 3. ¯ö¿¯
selected_page.run()