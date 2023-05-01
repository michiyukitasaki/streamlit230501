import streamlit as st

from show_page_notionDB import show_data_on_streamlit
from show_page_wieght import weight_app

# ページの選択肢
page = st.sidebar.radio('ページを選択してください:', ('体重管理', '資産管理'))

# ページに応じた操作
if page == '体重管理':
    weight_app()

elif page == '資産管理':
    show_data_on_streamlit()