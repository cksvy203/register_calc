import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def get_resistance_value(image_path):
    # 이미지 불러오기
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to load the image. Please check the image path.")
        return None, None, None

    # 이미지를 HSV 색 공간으로 변환
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 색상 범위 지정
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    lower_orange = np.array([11, 100, 100])
    upper_orange = np.array([20, 255, 255])
    lower_yellow = np.array([21, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    lower_green = np.array([31, 100, 100])
    upper_green = np.array([80, 255, 255])
    lower_blue = np.array([101, 100, 100])
    upper_blue = np.array([130, 255, 255])
    lower_violet = np.array([131, 100, 100])
    upper_violet = np.array([160, 255, 255])
    lower_gray = np.array([161, 100, 100])
    upper_gray = np.array([179, 255, 255])

    # 색상을 마스킹하여 각 색상 영역 추출
    red_mask = cv2.inRange(hsv_img, lower_red, upper_red)
    orange_mask = cv2.inRange(hsv_img, lower_orange, upper_orange)
    yellow_mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
    green_mask = cv2.inRange(hsv_img, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv_img, lower_blue, upper_blue)
    violet_mask = cv2.inRange(hsv_img, lower_violet, upper_violet)
    gray_mask = cv2.inRange(hsv_img, lower_gray, upper_gray)

    # 각 색상 영역에서 가장 큰 영역 추출
    colors = {
        "red": red_mask,
        "orange": orange_mask,
        "yellow": yellow_mask,
        "green": green_mask,
        "blue": blue_mask,
        "violet": violet_mask,
        "gray": gray_mask
    }
    max_area = 0
    max_color = None
    for color, mask in colors.items():
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contour_area = max([cv2.contourArea(contour) for contour in contours])
            if contour_area > max_area:
                max_area = contour_area
                max_color = color

    # 저항 값 계산
    resistor_values = {
        "black": 0,
        "brown": 1,
        "red": 2,
        "orange": 3,
        "yellow": 4,
        "green": 5,
        "blue": 6,
        "violet": 7,
        "gray": 8,
        "white": 9
    }

    color1, color2, multiplier, tolerance = max_color, "black", 1, 20  # 기본값 설정
    if max_color:
        # 두 번째 색상 결정
        if max_color == "yellow" or max_color == "white":
            color2 = "brown"
        elif max_color == "green":
            color2 = "blue"
        elif max_color == "blue":
            color2 = "violet"
        
        # 곱하기 결정
        if max_color == "black" or max_color == "gray" or max_color == "white":
            multiplier = 0
        elif max_color == "brown":
            multiplier = 1
        elif max_color == "red":
            multiplier = 2
        elif max_color == "orange":
            multiplier = 3
        elif max_color == "yellow":
            multiplier = 4
        elif max_color == "green":
            multiplier = 5
        elif max_color == "blue":
            multiplier = 6
        elif max_color == "violet":
            multiplier = 7
    else:
        print("Failed to detect resistance color.")
        return None, None, None

    resistance_value = (resistor_values[color1] * 10 + resistor_values[color2]) * 10**multiplier
    tolerance = 20  # 허용 오차는 기본값으로 설정
    if resistance_value >= 1000000:
        resistance_value /= 1000000
        unit = "m"
    elif resistance_value >= 1000:
        resistance_value /= 1000
        unit = "k"
    return resistance_value, unit, tolerance

class ResistanceApp:
    def __init__(self, master):
        self.master = master
        master.title("Resistance Calculator")
        master.geometry("300x300")

        self.label = tk.Label(master, text="Select an image:")
        self.label.pack()

        self.select_button = tk.Button(master, text="Select Image", command=self.select_image)
        self.select_button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.quit_button = tk.Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            resistance_value, unit, tolerance = get_resistance_value(file_path)
            if resistance_value is not None:
                self.result_label.config(text=f"Resistance Value: {resistance_value} {unit}Ω\nTolerance: {tolerance}%")
            else:
                self.result_label.config(text="Failed to detect resistance color.")

root = tk.Tk()
app = ResistanceApp(root)
root.mainloop()
