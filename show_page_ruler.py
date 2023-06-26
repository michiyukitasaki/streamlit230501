import pandas as pd
import streamlit as st
import cv2
import numpy as np
from PIL import Image

from RulerApp.ruler_method import detect_ruler_and_calculate_ratio, measure_object


def ruler_app():
    # UIの作成
    st.title("テスト用")

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)

    st.header("1. 背景画像をアップロード")
    background_image = st.file_uploader("背景画像を選択してください", type=["png", "jpg", "jpeg"])

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)

    st.header("2. 定規画像をアップロード")
    ruler_image = st.file_uploader("定規画像を選択してください", type=["png", "jpg", "jpeg"])
    # ruler_length = st.slider("定規の長さ（cm）", 10.0, 25.0, step=0.1)
    ruler_length = st.text_input("定規の長さ（cm）", value=float(15.0))
    ruler_length = float(ruler_length)

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)

    st.header("3. 測定対象画像をアップロード")
    object_image = st.file_uploader("測定対象画像を選択してください", type=["png", "jpg", "jpeg"])

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)


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
            if ruler_length is None:
                st.warning("定規の長さを選択してください。")
            else:
                # 画像をOpenCV形式に変換
                background_image = Image.open(background_image).convert("RGB")
                background_image = np.array(background_image)
                background_image = background_image[:, :, ::-1].copy()

                ruler_image = Image.open(ruler_image).convert("RGB")
                ruler_image = np.array(ruler_image)
                ruler_image = ruler_image[:, :, ::-1].copy()

                # スペースと境界線を追加します。
                st.markdown("<hr/>", unsafe_allow_html=True)

                # 処理Aの実行
                ratio,marked_ruler_image = detect_ruler_and_calculate_ratio(background_image, ruler_image, ruler_length)
                st.header("4. 正しく定規が検出できたかを確認してください")
                st.image(marked_ruler_image, caption="定規画像")

                #st.header("この定規画像でよろしいでしょうか？")
                # confirm_ruler_image = st.button("はい")
                # not_confirm_ruler_image = st.button("いいえ")


                # confirm_ruler_image = st.radio("この定規画像でよろしいですか？", ("はい", "いいえ"))
                #

                if object_image is not None :
                    # スペースと境界線を追加します。
                    st.markdown("<hr/>", unsafe_allow_html=True)
                    st.header("5. 測定結果")
                    # 画像をOpenCV形式に変換
                    object_image = Image.open(object_image).convert("RGB")
                    object_image = np.array(object_image)
                    object_image = object_image[:, :, ::-1].copy()

                    if ratio is not None:
                        perimeter_cm, width_cm, height_cm, area_cm2, result_image, _, _ = measure_object(background_image,object_image, ratio, False)

                        st.image(result_image, caption="測定結果")

                        # 長辺と短辺を判断します。
                        long_side_cm = max(width_cm, height_cm)
                        short_side_cm = min(width_cm, height_cm)

                        # 一覧表を作成
                        measurements_df = pd.DataFrame({
                            "項目": ["周囲の長さ[cm]", "長辺[cm]", "短辺[cm]", "面積[cm^2]"],
                            "値": [f"{perimeter_cm:.2f}", f"{long_side_cm:.2f}", f"{short_side_cm:.2f}", f"{area_cm2:.2f} "]
                        })

                        # 一覧表を表示
                        st.table(measurements_df)
                    else:
                        st.warning("定規の長さを指定してください。")