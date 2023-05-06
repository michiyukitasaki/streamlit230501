import base64

import pandas as pd
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import zipfile

from RulerApp.ruler_method import detect_ruler_and_calculate_ratio, measure_object


def ruler_multiple_app():
    # UIの作成
    st.title("定規アプリ")

    st.header("1. 背景画像をアップロード")
    background_image = st.file_uploader("背景画像を選択してください", type=["png", "jpg", "jpeg"])

    st.header("2. 定規画像をアップロード")
    ruler_image = st.file_uploader("定規画像を選択してください", type=["png", "jpg", "jpeg"])

    st.header("3. 測定対象画像をアップロード")
    uploaded_files = st.file_uploader("複数の物体画像を選択してください（フォルダ内のすべての画像を選択）", type=["png", "jpg", "jpeg"], accept_multiple_files=True)



    if background_image is not None and ruler_image is not None and uploaded_files is not None:
        # ボタンのサイズを変更するCSSを追加
        st.markdown("""
            <style>
                .stButton>button {
                    width: 200px;
                    height: 50px;
                    background-color: #4CAF50;
                    color: white;
                    font-size: 1.5em;
                    margin: 0 auto;
                    display: block;
                }
            </style>
        """, unsafe_allow_html=True)
        process_images = st.button("測定開始")

        if process_images:
            # 結果を格納するデータフレームを作成
            result_df = pd.DataFrame(columns=["ファイル名", "外周[cm]", "幅[cm]", "高さ[cm]", "面積[cm^2]"])

            # 画像をOpenCV形式に変換
            background_image = Image.open(background_image).convert("RGB")
            background_image = np.array(background_image)
            background_image = background_image[:, :, ::-1].copy()

            ruler_image = Image.open(ruler_image).convert("RGB")
            ruler_image = np.array(ruler_image)
            ruler_image = ruler_image[:, :, ::-1].copy()

            # 処理Aの実行
            ratio,marked_ruler_image = detect_ruler_and_calculate_ratio(background_image, ruler_image)
            st.header("4. 正しく定規が検出できたかを確認してください")
            st.image(marked_ruler_image, caption="定規画像")


            if uploaded_files is not None :

                for uploaded_file in uploaded_files:
                    # 画像をOpenCV形式に変換
                    object_image = Image.open(uploaded_file).convert("RGB")
                    object_image = np.array(object_image)
                    object_image = object_image[:, :, ::-1].copy()

                    # 測定を実行
                    perimeter_cm, width_cm, height_cm, area_cm2, _ = measure_object(background_image, object_image,
                                                                                    ratio)

                    # 結果をデータフレームに追加
                    result_df = pd.concat([result_df, pd.DataFrame({
                        "ファイル名": [uploaded_file.name],
                        "外周[cm]": [perimeter_cm],
                        "幅[cm]": [width_cm],
                        "高さ[cm]": [height_cm],
                        "面積[cm^2]": [area_cm2]
                    })], ignore_index=True)

                result_df = result_df.round(2) # 小数点以下2桁に丸める
                summary_df = result_df.describe()  # 統計量を計算

                st.header("5. 測定結果")
                st.write(result_df) # 測定結果をブラウザに表示

                st.header("6. 統計結果")
                st.dataframe(summary_df) # 統計結果をブラウザに表示

                # 測定結果を CSV に変換
                result_csv = result_df.to_csv(index=True)
                result_csv_bytes = result_csv.encode()

                # 統計結果を CSV に変換
                summary_csv = summary_df.to_csv(index=True)
                summary_csv_bytes = summary_csv.encode()

                # CSVファイルを含むZIPファイルを作成
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zf:
                    zf.writestr("measurement_results.csv", result_csv_bytes)
                    zf.writestr("summary_statistics.csv", summary_csv_bytes)


                # ダウンロードボタンを表示
                zip_buffer.seek(0)
                download_button = st.download_button(
                    label="測定結果と統計結果をダウンロード",
                    data=zip_buffer,
                    file_name="results.zip",
                    mime="application/zip",
                )
                if download_button:
                    st.write("結果がダウンロードされました。")


