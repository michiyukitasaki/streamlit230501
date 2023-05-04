import numpy as np
import streamlit as st
from PIL import Image
import pytesseract
import cv2
from pytesseract import image_to_string

def ocr_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang='jpn')
    return text

def ocr_app():
    st.title('OCR with Streamlit')
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Recognized Text:")
        text = ocr_image(img_array)
        st.text_area("", text, height=200)  # textareaでコピー可能なテキストを表示します。
