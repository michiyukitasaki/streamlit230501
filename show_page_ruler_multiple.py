# 必要なライブラリをインポートします。
import base64
import pandas as pd
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import zipfile

# 自作のモジュールをインポートします。このモジュールには、定規の検出と比率の計算、物体の測定といった関数が含まれています。
from RulerApp.ruler_method import detect_ruler_and_calculate_ratio, measure_object

# アプリケーションのメイン関数を定義します。
def ruler_multiple_app():
    # UIの作成
    st.title("長辺・短辺・高さ・面積測定アプリ") # タイトルを設定します。

    # アプリケーションの説明を表示します。
    st.markdown("このアプリケーションでは複数枚のパンの画像をアップロードすると自動で長辺・短辺・面積・統計結果を取得することができます。", unsafe_allow_html=True)

    # カスタムスタイルを定義します。このスタイルは後でガイダンスセクションに適用されます。
    style = """
    <style>
    .guidance {
        background-color: #009999;
        padding: 20px;
        border-radius: 100px;
    }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True) # スタイルを適用します。

    # 使い方ガイドを表示します。
    st.header("使い方ガイド")

    # ガイダンスセクションの各ステップを表示します。
    st.markdown(
        "<div class='guidance'>このアプリでは、背景画像と定規画像をアップロードし、物体の寸法を測定できます。以下の手順に従って操作してください。</div>",
        unsafe_allow_html=True)

    # 各ステップの詳細を表示します。
    st.markdown("<div class='guidance'>1. [背景画像アップロード] ボタンをクリックし、背景画像をアップロードします。</div>", unsafe_allow_html=True)
    st.markdown("<div class='guidance'>2. [定規画像アップロード] ボタンをクリックし、定規画像をアップロードします。</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='guidance'>3. [測定対象画像アップロード] ボタンをクリックして測定対象画像をアップロードします。</div>",
        unsafe_allow_html=True)
    st.markdown("<div class='guidance'>4. 背景画像、定規画像、測定対象画像（複数枚OK）がアップロードされたら、[測定開始] ボタンをクリックします。</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='guidance'>5. 測定結果と統計結果が表示されます。</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='guidance'>6. 測定結果をCSVファイルとしてダウンロードするには、[測定結果と統計結果をダウンロード] ボタンをクリックします。</div>",
                unsafe_allow_html=True)

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)

    # 背景画像、定規画像、測定対象画像のアップロードセクションを作成します。
    # col5, col6 = st.columns([1, 3])
    # 左側の列に画像を配置します。
    # col5.image("/home/user/Image/White.jpeg", width=100)
    st.header("①. 背景画像をアップロード")
    background_image = st.file_uploader("背景画像を選択してください", type=["png", "jpg", "jpeg"])

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)

    # 背景画像、定規画像、測定対象画像のアップロードセクションを作成します。
    # col1, col2 = st.columns([1, 3])
    # 左側の列に画像を配置します。
    # col1.image("/home/user/Image/Ruler.jpg", width=100)

    st.header("②. 定規画像をアップロード")
    ruler_image = st.file_uploader("定規画像を選択してください", type=["png", "jpg", "jpeg"])

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)

    # 背景画像、定規画像、測定対象画像のアップロードセクションを作成します。
    # col3, col4 = st.columns([1, 3])
    # 左側の列に画像を配置します。
    # col3.image("/home/user/Image/Pan.jpeg", width=100)
    st.header("③. パン画像（複数枚OK）をアップロード")
    uploaded_files = st.file_uploader("複数の物体画像を選択してください（フォルダ内のすべての画像を選択）", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    # スペースと境界線を追加します。
    st.markdown("<hr/>", unsafe_allow_html=True)

    # すべての画像がアップロードされたら、測定を開始するボタンを表示します。
    if background_image is not None and ruler_image is not None and uploaded_files is not None:
        process_images = st.button("測定開始")

        # ボタンがクリックされたら、測定を開始します。
        if process_images:
            # 結果を格納するデータフレームを作成します。
            result_df = pd.DataFrame(columns=["ファイル名", "外周[cm]", "長辺[cm]", "短辺[cm]", "面積[cm^2]"])

            # 画像をOpenCV形式に変換します。
            background_image = Image.open(background_image).convert("RGB")
            background_image = np.array(background_image)
            background_image = background_image[:, :, ::-1].copy()

            ruler_image = Image.open(ruler_image).convert("RGB")
            ruler_image = np.array(ruler_image)
            ruler_image = ruler_image[:, :, ::-1].copy()

            # スペースと境界線を追加します。
            st.markdown("<hr/>", unsafe_allow_html=True)

            # 定規を検出し、比率を計算します。
            ratio,marked_ruler_image = detect_ruler_and_calculate_ratio(background_image, ruler_image)
            st.header("④. 正しく定規が検出できたかを確認してください")
            st.image(marked_ruler_image, caption="定規画像")

            # 測定対象画像がアップロードされている場合、それぞれの画像に対して測定を行います。
            if uploaded_files is not None :
                for uploaded_file in uploaded_files:
                    # 画像をOpenCV形式に変換します。
                    object_image = Image.open(uploaded_file).convert("RGB")
                    object_image = np.array(object_image)
                    object_image = object_image[:, :, ::-1].copy()

                    # 測定を実行します。
                    perimeter_cm, width_cm, height_cm, area_cm2, _ = measure_object(background_image, object_image,
                                                                                    ratio)

                    # 長辺と短辺を判断します。
                    long_side_cm = max(width_cm, height_cm)
                    short_side_cm = min(width_cm, height_cm)

                    # 結果をデータフレームに追加します。
                    result_df = pd.concat([result_df, pd.DataFrame({
                        "ファイル名": [uploaded_file.name],
                        "外周[cm]": [perimeter_cm],
                        "長辺[cm]": [long_side_cm],
                        "短辺[cm]": [short_side_cm],
                        "面積[cm^2]": [area_cm2]
                    })], ignore_index=True)

                # 結果を小数点以下2桁に丸めます。
                result_df = result_df.round(2)
                # 統計量を計算します。
                summary_df = result_df.describe().round(2)

                # スペースと境界線を追加します。
                st.markdown("<hr/>", unsafe_allow_html=True)

                # 測定結果と統計結果を表示します。
                st.header("⑤. 測定結果")
                st.write(result_df)

                # スペースと境界線を追加します。
                st.markdown("<hr/>", unsafe_allow_html=True)

                st.header("⑥. 統計結果")
                st.dataframe(summary_df)

                # 測定結果と統計結果をCSVファイルに変換します。
                result_csv = result_df.to_csv(index=True)
                result_csv_bytes = result_csv.encode()
                summary_csv = summary_df.to_csv(index=True)
                summary_csv_bytes = summary_csv.encode()

                # CSVファイルを含むZIPファイルを作成します。
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zf:
                    zf.writestr("measurement_results.csv", result_csv_bytes)
                    zf.writestr("summary_statistics.csv", summary_csv_bytes)

                # ダウンロードボタンを表示します。
                zip_buffer.seek(0)
                download_button = st.download_button(
                    label="測定結果と統計結果をダウンロード",
                    data=zip_buffer,
                    file_name="results.zip",
                    mime="application/zip",
                )
                if download_button:
                    st.write("結果がダウンロードされました。")
