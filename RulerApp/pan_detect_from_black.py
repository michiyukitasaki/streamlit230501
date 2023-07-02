import cv2
import numpy as np
from PIL import Image

def remove_black_background_and_display(img, isShow=False):
    # 色範囲を設定する
    #黒
    lower_val = np.array([0,0,0])
    upper_val = np.array([180,180,180])

    #青
    # lower_val = np.array([100, 0, 0])
    # upper_val = np.array([255, 100, 100])
    #オレンジ
    # lower_val = np.array([0, 100, 200])
    # upper_val = np.array([50, 150, 255])
    #緑
    # lower_val = np.array([0, 100, 0])
    # upper_val = np.array([100, 255, 100])

    # 黒色の部分をマスクする
    mask = cv2.inRange(img, lower_val, upper_val)

    # マスクを適用して黒色の部分を白色にする
    img[mask == 255] = [255, 255, 255]
    return img

    if(isShow == True):
        cv2.imshow("Result", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    image = Image.open('/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/Image/0630Test/0702.jpg').convert("RGB")
    image = np.array(image)
    image = image[:, :, ::-1].copy()  # Convert RGB to BGR
    remove_black_background_and_display(image, isShow=True)