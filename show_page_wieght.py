import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

def weight_app():
    # タイトル
    st.title('体重管理アプリ')

    # 複数日の体重データを入力するためのフィールドを作成
    num_days = st.number_input('何日分のデータを入力しますか？', min_value=1, value=1, step=1)  # 日数を入力

    # フィールドの値を保存するための辞書を初期化
    input_data = {'Date': [], 'Weight': []}

    columns = st.columns(2)
    for i in range(num_days):
        date = columns[0].date_input(f'日付 {i + 1} を選択してください', key=f'date_{i + 1}')  # 日付を入力
        weight = columns[1].number_input(f'体重 {i + 1} を入力してください (kg)', min_value=0.0, step=0.1,
                                         key=f'weight_{i + 1}')  # 体重を入力
        input_data['Date'].append(date)
        input_data['Weight'].append(weight)

    # 体重データを保存するDataFrameを初期化
    if 'weight_data' not in st.session_state:
        if os.path.isfile('weight_data4.csv'):
            st.session_state['weight_data'] = pd.read_csv('weight_data4.csv')  # 保存されているDataFrameを取得
        else:
            st.session_state['weight_data'] = pd.DataFrame(
                columns=['Date', 'Weight'])  # 保存されているDataFrameがない場合は空のDataFrameを作成

    # 入力データをDataFrameに追加
    if st.button('追加'):
        new_data = pd.DataFrame(input_data)
        df = st.session_state['weight_data']  # 保存されているDataFrameを取得
        df['Date'] = pd.to_datetime(df['Date'])  # 日付をdatetime型に変換
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d') # 日付を文字列型に変換
        df = pd.concat([df, new_data], ignore_index=True)  # 保存されているDataFrameと新しく入力されたDataFrameを結合
        st.session_state['weight_data'] = df  # 結合したDataFrameを保存
        df.to_csv('weight_data4.csv', index=False)  # 保存

    # DataFrameを表示
    df = st.session_state['weight_data'] # 保存されているDataFrameを取得
    df['Date'] = pd.to_datetime(df['Date']) # 日付をdatetime型に変換
    st.dataframe(df.style.highlight_max(axis=0))

    # グラフを描画
    if not st.session_state['weight_data'].empty:
        st.subheader('体重の変化')
        fig, ax = plt.subplots()

        st.session_state['weight_data']['Date'] = pd.to_datetime(st.session_state['weight_data']['Date'])
        st.session_state['weight_data'].plot(kind='scatter', x='Date', y='Weight', ax=ax)

        # x軸の目盛りを10日ごとに設定
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=15))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        st.pyplot(fig)
