import streamlit as st
import requests
import json

def qiita_api():
    # タイトルを表示
    st.title('Qiita検索アプリ')

    # 検索ボックスを作成
    keyword = st.text_input('キーワードを入力してください')

    # 検索ボタンを作成
    if st.button('検索'):
        # Qiita APIからデータを取得
        response = requests.get(f'https://qiita.com/api/v2/items?page=1&per_page=20&query={keyword}')

        # レスポンスが200 OKの場合、データを取得
        if response.status_code == 200:
            # レスポンスを解析
            articles = json.loads(response.text)

            # ライク数でソートして上位の記事を表示
            articles_sorted_by_likes = sorted(articles, key=lambda x: x['likes_count'], reverse=True)

            # データを整形して表示
            for article in articles_sorted_by_likes[:5]:  # 上位5記事を表示
                st.write(f"タイトル: {article['title']}")
                st.write(f"ライク数: {article['likes_count']}")
                st.write(f"URL: {article['url']}")
                st.write("---")
        else:
            st.write('Error: API request failed.')

