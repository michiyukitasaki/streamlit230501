import streamlit as st
import pandas as pd

from SubMethod.get_gsName_fromDrive import list_google_drive_files

# ここでは、titlesとidsというリストがすでに作成されていると仮定しています。
titles = ['Title1', 'Title2', 'Title3']  # これらのリストを実際のデータで置き換えます。
ids = ['ID1', 'ID2', 'ID3']

# Dataframeを作成します。
df = pd.DataFrame({
    'Title': titles,
    'ID': ids,
})



def gs_app():

    st.title('Google Driveのファイル一覧')

    # セレクトボックスの選択肢
    options = ["スプレッドシート", "ドキュメント", "スライド"]

    # セレクトボックスを作成（デフォルトの選択肢は"ドキュメント"）
    default_index = options.index("ドキュメント")
    choice = st.selectbox("選択してください：", options, index=default_index)

    if st.button('ファイルリスト取得'): # ボタンが押されたら、以下のコードが実行されます。
        file_list = list_google_drive_files(choice) # ここで、Google Driveのファイル一覧を取得する関数を呼び出します。
        df = pd.DataFrame(file_list) # 取得したファイル一覧をデータフレームに変換します。
        df = df[['title', 'id']] # titleとidの列だけを残します。
        st.dataframe(df) # データフレームを表示します。



