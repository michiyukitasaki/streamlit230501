import cv2



def detect_and_fill(img_array, actual_length, scale_factor=None):
    threshold = 150

    img_color = img_array.copy()
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.blur(img_gray, (9, 9))
    ret, img_binary = cv2.threshold(img_blur, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 最大の輪郭を見つける
    largest_contour = max(contours, key=cv2.contourArea)

    # 最大の輪郭の面積を取得
    area_pixel = cv2.contourArea(largest_contour)

    # 最大の輪郭が囲む領域を塗りつぶす
    cv2.drawContours(img_color, [largest_contour], 0, (0, 255, 0), thickness=-1)


    # 最大の輪郭を囲む矩形を取得
    x, y, w, h = cv2.boundingRect(largest_contour)

    # 矩形の長辺と短辺を計算
    long_side = max(w, h)
    short_side = min(w, h)

    # スケールファクタが与えられていない場合、計算します
    if scale_factor is None:
        scale_factor = actual_length / long_side

    # 矩形の長辺と短辺を計算し、実際のcmに変換
    long_side_cm = long_side * scale_factor
    short_side_cm = short_side * scale_factor

    area_cm2 = area_pixel * (scale_factor ** 2)

    # 矩形を描画
    cv2.rectangle(img_color, (x, y), (x+w, y+h), (255, 0, 0), 5)

    # 長辺と短辺の長さを画像に記載
    cv2.putText(img_color, f"Long: {long_side_cm:.1f}cm", (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
    cv2.putText(img_color, f"Short: {short_side_cm:.1f}cm", (x, y-130), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)
    cv2.putText(img_color, f"Area: {area_cm2:.1f}cm2", (x, y - 220), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

    cv2.imwrite("stone_with_rectangle.jpeg", img_color)
    return img_color, long_side_cm, short_side_cm, area_cm2, long_side

if __name__ == "__main__":
    # img = "/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/Image/Pan/Width/unnamed.jpg"
    img_1 = "/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/Image/Pan/Width/unnamed (1).jpg"
    detect_and_fill(img_1)