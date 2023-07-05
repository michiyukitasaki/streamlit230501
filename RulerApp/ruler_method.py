import cv2
import numpy as np

def detect_ruler_and_calculate_ratio(bg_image, ruler_image, ruler_length, show_diff=False, show_marked_ruler=False):
    # 画像をグレースケールに変換12
    bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
    ruler_gray = cv2.cvtColor(ruler_image, cv2.COLOR_BGR2GRAY)

    # # ガウシアンブラーを適用
    # bg_gray = cv2.GaussianBlur(bg_gray, (5, 5), 0)
    # ruler_gray = cv2.GaussianBlur(ruler_gray, (5, 5), 0)

    # 二つの画像間の絶対差分を計算
    diff = cv2.absdiff(bg_gray, ruler_gray)

    # 差分画像に閾値処理を適用
    threshold_value = 15
    _, thresholded_diff = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)

    # アダプティブ閾値処理を適用
    # thresholded_diff = cv2.adaptiveThreshold(diff, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    if show_diff:
        cv2.imshow("閾値処理された差分画像", thresholded_diff)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 閾値処理された差分画像で輪郭を検出
    contours, _ = cv2.findContours(thresholded_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 最大面積の輪郭を見つける（定規と仮定）
    max_area = 0
    ruler_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            ruler_contour = contour

    # 定規の輪郭の外接矩形を計算
    x, y, w, h = cv2.boundingRect(ruler_contour)

    # 外接矩形の最長辺の長さを計算
    longest_side = max(w, h)

    # 定規の長さ（センチメートル）をピクセルで割って比率を計算
    ruler_length_cm = ruler_length
    ratio = ruler_length_cm / longest_side

    # (戻り値)定規の最長辺に沿って矢印を描画
    marked_ruler_image = ruler_image.copy()
    if longest_side == w: # 横長の場合
        cv2.arrowedLine(marked_ruler_image, (x, y + h // 2), (x + w, y + h // 2), (0, 255, 0), 2, cv2.LINE_AA)
    else: # 縦長の場合
        cv2.arrowedLine(marked_ruler_image, (x + w // 2, y), (x + w // 2, y + h), (0, 255, 0), 2, cv2.LINE_AA)

    # （画像表示）定規の最長辺に沿って矢印を描画
    if show_marked_ruler:
        marked_ruler_image = ruler_image.copy()
        if longest_side == w:
            cv2.arrowedLine(marked_ruler_image, (x, y + h//2), (x + w, y + h//2), (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.arrowedLine(marked_ruler_image, (x + w//2, y), (x + w//2, y + h), (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("マーク付き定規", marked_ruler_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return ratio, marked_ruler_image





def measure_object(bg_image, object_image, ratio, show_result=False):
    # 画像をグレースケールに変換
    bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
    object_gray = cv2.cvtColor(object_image, cv2.COLOR_BGR2GRAY)

    # # ガウシアンブラーを適用
    # bg_gray = cv2.GaussianBlur(bg_gray, (5, 5), 0)
    # object_gray = cv2.GaussianBlur(object_gray, (5, 5), 0)

    # 二つの画像間の絶対差分を計算
    diff = cv2.absdiff(bg_gray, object_gray)

    # 差分画像に閾値処理を適用
    threshold_value = 15
    _, thresholded_diff = cv2.threshold(diff, threshold_value, 255, cv2.THRESH_BINARY)

    # 閾値処理された差分画像で輪郭を検出
    contours, _ = cv2.findContours(thresholded_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)



    # 最大面積の輪郭を見つける（物体と仮定）
    max_area = 0
    object_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            object_contour = contour

    # 物体の輪郭の外接矩形を計算
    x, y, w, h = cv2.boundingRect(object_contour)

    # 外接矩形の縦と横の長さを実際の長さに変換
    width_cm = w * ratio
    height_cm = h * ratio

    # 物体の面積を計算
    area_cm2 = max_area * (ratio ** 2)

    # 物体の外周を計算
    perimeter_cm = cv2.arcLength(object_contour, True) * ratio

    # 寸法を画像に描画する
    result_image = object_image.copy()
    # cv2.putText(result_image, f"Width: {width_cm:.2f} cm", (x, y + h + 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 51, 0), 5)
    # cv2.putText(result_image, f"Height: {height_cm:.2f} cm", (x, y + h + 570), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 51, 0), 5)
    # cv2.putText(result_image, f"Area: {area_cm2:.2f} cm^2", (x, y + h + 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 51, 0), 5)
    # cv2.putText(result_image, f"Perimeter: {perimeter_cm:.2f} cm", (x, y + h + 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 51, 0), 5)

    # 最小外接矩形を取得
    rect = cv2.minAreaRect(object_contour)

    # 四角形の頂点座標を取得
    box = cv2.boxPoints(rect)
    box = np.intp(box)  # ここをnp.intpに変更

    # 外周をラインで囲む色 (BGR)
    contour_color = (255, 51, 0)

    # 外周をラインで囲む太さ
    contour_thickness = 5

    # 外周をラインで囲む
    cv2.drawContours(result_image, [box], 0, contour_color, contour_thickness)

    # 結果を表示する
    if show_result:
        # 外周をラインで囲む色 (BGR)
        contour_color = (255, 51, 0)

        # 外周をラインで囲む太さ
        contour_thickness = 3

        # 差分画像を表示
        cv2.imshow("Diff", diff)
        cv2.imshow("Thresholded Diff", thresholded_diff)
        cv2.imshow("Result", result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return perimeter_cm, width_cm, height_cm, area_cm2, result_image, diff, thresholded_diff


if __name__ == "__main__":
    bg_image = cv2.imread("/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/Image/PanTest_0622/BackGround.jpg")
    ruler_image = cv2.imread("/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/Image/PanTest_0622/Ruler.jpg")
    # object_img = cv2.imread("/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/Image/PanTest_0622/Pan.jpg")
    object_img = cv2.imread("/Volumes/SSD-PUTU3C/pythonProject/Streamlit0501/Image/Pan/Width/1687261523448.jpg")

    ratio, marked_ruler_image = detect_ruler_and_calculate_ratio(bg_image, ruler_image, show_diff=True, show_marked_ruler=True)
    print("Length per pixel: {:.4f} cm".format(ratio))

    perimeter, width, height, area, result_image, diff, thresholded_diff = measure_object(bg_image, object_img, ratio, show_result=True)

    # 長辺と短辺を判断します。
    long_side_cm = max(width, height)
    short_side_cm = min(width, height)

    # 結果を表示する
    print("物体の外周: {:.2f} cm".format(perimeter))
    print("長辺: {:.2f} cm".format(long_side_cm))
    print("短辺: {:.2f} cm".format(short_side_cm))
    print("物体の面積: {:.2f} cm".format(area))

    # 結果画像を表示する
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresholded Diff", thresholded_diff)
    cv2.imshow("Result Image", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
