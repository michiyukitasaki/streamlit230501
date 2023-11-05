import base64

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from detect_for_opencv import detect_and_fill
import pandas as pd
import zipfile
import io

# def ruler_ui_mainpage():
#     st.title("Object Detection and Measurement")
#
#     uploaded_file = st.file_uploader("Choose an image...", type="jpg")
#
#     # UIから物体の実際の長さを入力
#     actual_length = st.text_input("Enter the actual length of the object (in your preferred unit):")
#
#     if uploaded_file is not None and actual_length:
#         actual_length = float(actual_length)
#
#         img = Image.open(uploaded_file)
#         img_array = np.array(img)
#
#         st.image(img, caption='Uploaded Image.', use_column_width=True)
#         st.write("")
#         st.write("Detecting...")
#
#         result_img, detected_long_side = detect_and_fill(img_array, actual_length)
#         if result_img is not None:
#             st.image(result_img, caption='Detected Image.', use_column_width=True)
#
#
#
#         # st.write(f"1 pixel corresponds to {scale_factor:.2f} units")

def ruler_ui_mainpage():
    # UIの作成2
    st.title("長辺・短辺・面積測定アプリ")  # タイトルを設定します。

    # アプリケーションの説明を表示します。
    st.markdown("このアプリケーションでは複数枚のパンの画像をアップロードすると自動で長辺・短辺・面積・統計結果を取得することができます。",
                unsafe_allow_html=True)

    # カスタムスタイルを定義します。このスタイルは後でガイダンスセクションに適用されます。
    style = """
        <style>
        .guidance {
            background-color: #009999;
            padding: 20px;
            # border-radius: 100px;
        }
        </style>
        """
    st.markdown(style, unsafe_allow_html=True)  # スタイルを適用します。

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)

    # 使い方ガイドを表示します。
    st.header("使い方ガイド")


    # 各ステップの詳細を表示します。
    st.markdown("<div class='guidance'>1. パンが写っている画像をアップロードします。（複数枚OK）。</div>", unsafe_allow_html=True)
    st.markdown("<div class='guidance'>2. 1枚目の画像に写っているパンの長い方の辺の長さ(cm)を入力します。</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='guidance'>3. [解析開始]ボタンをクリックします。</div>",
        unsafe_allow_html=True)
    st.markdown(
        "<div class='guidance'>4. 処理された画像が表示されます。</div>",
        unsafe_allow_html=True)
    st.markdown("<div class='guidance'>5. [結果ダウンロード]ボタンをクリックすると測定結果と統計結果をダウンロードすることができます。</div>",
                unsafe_allow_html=True)

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader("画像を選択してください...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    results = []

    # 1つもファイルがアップロードされていない場合
    if not uploaded_files:
        return

    # UIから物体の実際の長さを入力
    actual_length = st.text_input("長辺の長さ(cm)を入力してください")

    if not actual_length:
        st.warning("長辺の長さ(cm)を入力してください")
        return

    # 「解析開始」ボタンを追加
    if st.button('解析開始'):
        actual_length = float(actual_length)

        results = []
        scale_factor = None

        for i, uploaded_file in enumerate(uploaded_files):
            img = Image.open(uploaded_file)
            img_array = np.array(img)

            if i == 0:  # 1枚目の画像
                st.image(img, caption='Uploaded Image.', use_column_width=True)
                st.write("Detecting for calibration...")
                result_img, long_side_cm, short_side_cm, area_cm2,detected_long_side = detect_and_fill(img_array, actual_length)
                scale_factor = actual_length / detected_long_side
            else:
                st.image(img, caption='Uploaded Image.', use_column_width=True)
                st.write("Detecting using calibration from the first image...")
                result_img, long_side_cm, short_side_cm, area_cm2, _ = detect_and_fill(img_array, actual_length,scale_factor)

            if result_img is not None:
                st.image(result_img, caption='Detected Image.', use_column_width=True)

            # 画像ごとの結果を保存
            results.append({
                "File名": uploaded_file.name,
                "面積(cm^2)":round(area_cm2, 1),
                "長辺(cm)": round(long_side_cm, 1),
                "短辺(cm)": round(short_side_cm, 1)
            })

        # 統計情報をCSVとして出力
        df = pd.DataFrame(results)

        # 数値のみの列に絞り込む
        numeric_df = df.select_dtypes(include=['float64'])

        # 統計処理
        stats = {
            "最大":round(numeric_df.max()).tolist(),
            "最小": round(numeric_df.min()).tolist(),
            "平均": round(numeric_df.mean()).tolist(),
            "標準偏差": round(numeric_df.std()).tolist(),
        }
        stats_df = pd.DataFrame(stats, index=numeric_df.columns)

        # CSVファイルを保存するバッファを作成
        measurement_buffer = io.StringIO()
        stats_buffer = io.StringIO()

        # データフレームをCSVとしてバッファに保存
        df.to_csv(measurement_buffer, index=True)
        stats_df.to_csv(stats_buffer, index=True)

        # バッファの内容をZIPファイルにまとめる
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("measurement_results.csv", measurement_buffer.getvalue())
            zip_file.writestr("stats_results.csv", stats_buffer.getvalue())

        # ZIPファイルをbase64にエンコードしてダウンロードリンクを生成
        b64_zip = base64.b64encode(zip_buffer.getvalue()).decode()
        href_zip = f'<a href="data:application/zip;base64,{b64_zip}" download="results.zip">結果をダウンロード</a>'
        st.markdown(href_zip, unsafe_allow_html=True)