import streamlit as st

from show_page_finance import finance_app
from show_page_gDrive_gs import gs_app
from show_page_notionDB import show_data_on_streamlit
from show_page_ocr import ocr_app
from show_page_qiita import qiita_api
from show_page_ruler import ruler_app
from show_page_ruler_multiple import ruler_multiple_app
from show_page_wieght import weight_app


# ページの選択肢
# page = st.sidebar.radio('ページを選択してください:', ('体重管理', '資産管理', '株価管理', 'Qiita検索', 'スプレッドシート一覧','OCR処理', 'メジャーアプリ','メジャー（マルチ）アプリ'))
page = st.sidebar.radio('ページを選択してください:', ('テスト','測定アプリ'))
# # ページに応じた操作
# if page == '体重管理':
#     weight_app()
#
# elif page == '資産管理':
#     show_data_on_streamlit()
#
# elif page == '株価管理':
#     finance_app()
#
# elif page == 'Qiita検索':
#     qiita_api()
#
# elif page == 'スプレッドシート一覧':
#     gs_app()
#
# elif page == 'OCR処理':
#     ocr_app()

if page == 'テスト':
    ruler_app()

elif page == '測定アプリ':
    ruler_multiple_app()

# ruler_multiple_app()