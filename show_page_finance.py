import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr

def finance_app():
    # Streamlitのタイトルを設定
    st.title('株価ダッシュボード')

    # ユーザーに企業のティッカーシンボルを入力させる
    ticker = st.text_input('ティッカーシンボルを入力してください（例：GOOG）')


    if ticker:
        # yfinanceを使って株価データを取得
        data = yf.download(ticker, period='1y')

        if data.empty:
            st.write('無効なティッカーシンボル、またはデータが利用できません。')
        else:
            # データフレームを表示
            st.dataframe(data)

            # 終値のグラフを描画
            st.subheader('終値のグラフ')
            fig, ax = plt.subplots()
            data['Close'].plot(ax=ax)
            st.pyplot(fig)
