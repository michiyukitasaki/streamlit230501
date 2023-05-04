import streamlit as st

from show_page_finance import finance_app
from show_page_notionDB import show_data_on_streamlit
from show_page_qiita import qiita_api
from show_page_wieght import weight_app


# ページの選択肢
page = st.sidebar.radio('ページを選択してください:', ('体重管理', '資産管理', '株価管理', 'Qiita検索'))

# ページに応じた操作
if page == '体重管理':
    weight_app()

elif page == '資産管理':
    show_data_on_streamlit()

elif page == '株価管理':
    finance_app()

elif page == 'Qiita検索':
    qiita_api()
