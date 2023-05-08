import pandas as pd
import streamlit as st
import cv2
import numpy as np
from PIL import Image

from RulerApp.ruler_method import detect_ruler_and_calculate_ratio, measure_object


def ruler_app():
    # UIの作成
    st.title("メジャーアプリ（校正確認用）")

    st.header("1. 背景画像をアップロード")
    background_image = st.file_uploader("背景画像を選択してください", type=["png", "jpg", "jpeg"])

    st.header("2. 定規画像をアップロード")
    ruler_image = st.file_uploader("定規画像を選択してください", type=["png", "jpg", "jpeg"])

    st.header("3. 測定対象画像をアップロード")
    object_image = st.file_uploader("測定対象画像を選択してください", type=["png", "jpg", "jpeg"])


    if background_image is not None and ruler_image is not None and object_image is not None:
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

            #st.header("この定規画像でよろしいでしょうか？")
            # confirm_ruler_image = st.button("はい")
            # not_confirm_ruler_image = st.button("いいえ")


            # confirm_ruler_image = st.radio("この定規画像でよろしいですか？", ("はい", "いいえ"))
            #

            if object_image is not None :
                st.header("5. 測定結果")
                # 画像をOpenCV形式に変換
                object_image = Image.open(object_image).convert("RGB")
                object_image = np.array(object_image)
                object_image = object_image[:, :, ::-1].copy()

                perimeter_cm, width_cm, height_cm, area_cm2, result_image = measure_object(background_image,object_image, ratio)

                st.image(result_image, caption="測定結果")
                # 一覧表を作成
                measurements_df = pd.DataFrame({
                    "項目": ["周囲の長さ[cm]", "幅[cm]", "高さ[cm]", "面積[cm^2]"],
                    "値": [f"{perimeter_cm:.2f}", f"{width_cm:.2f}", f"{height_cm:.2f}", f"{area_cm2:.2f} "]
                })

                # 一覧表を表示
                st.table(measurements_df)
    #             st.write("周囲の長さ: {} cm".format(perimeter_cm))
    #             st.write("幅: {} cm".format(width_cm))
    #             st.write("高さ: {} cm".format(height_cm))
    #             st.write("面積: {} cm2".format(area_cm2))
    # #
    #
    # if not_confirm_ruler_image:
    #     st.warning("画像を再アップロードしてください。")
    #     st.experimental_rerun()