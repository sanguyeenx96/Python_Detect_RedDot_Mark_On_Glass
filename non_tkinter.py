import cv2
import numpy as np
import subprocess
import time
import keyboard

LOWER_RED = np.array([0, 100, 85]) # giá trị ngưỡng dưới (lower threshold) của màu đỏ trong HSV
UPPER_RED = np.array([10, 255, 255]) # giá trị ngưỡng trên (upper threshold) của màu đỏ trong HSV

def capture_image_with_fswebcam(output_path): # 1.chụp ảnh
    try:
        print("Đang chụp ảnh...")
        start_time = time.time()
        subprocess.run(['fswebcam', '-r', '1600x1200', '--no-banner', '--jpeg', '95', '-F', '8', output_path])
        end_time = time.time()
        timecount = end_time - start_time
        print("Thời gian chụp ảnh : ", timecount)
        crop_image(input_path=output_path, output_path='cropped.jpg', x=500, y=450, w=450, h=144)
    except Exception as e:
        print("Có lỗi xảy ra : ", e)

def crop_image(input_path, output_path, x, y, w, h): # 2.crop khu vực check
    try:
        image = cv2.imread(input_path)
        cropped_image = image[y:y+h, x:x+w]
        cv2.imwrite(output_path, cropped_image)
        checking(output_path)
    except Exception as e:
        print("Có lỗi xảy ra : ", e)

def checking(image_path): # 3.kiểm tra
    print("Đang kiểm tra...")
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    try:
        mask = cv2.inRange(hsv, LOWER_RED, UPPER_RED)
        red_sum = np.sum(image[mask > 0, 2]) #( 0: Blue, 1:Green, 2:Red)
        print(int(red_sum))
        giatri = int(red_sum)
        if giatri > 50:
            print("OK")
            write_text_on_image(image_path, "result_image.jpg", "OK!",(125, 246, 55))
            cv2.imshow("Kết quả", cv2.imread("result_image.jpg"))
            cv2.waitKey()
        else:
            print("NG")
            write_text_on_image(image_path, "result_image.jpg", "NG!", (o, o, 255))
            cv2.imshow("Kết quả", cv2.imread("result_image.jpg"))
            cv2.waitKey()
    except Exception as e:
        print("Có lỗi xảy ra : ", e)

def write_text_on_image(input_path, output_path, text,color):
    image = cv2.imread(input_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = color
    thickness = 4
    position = (100, 35)
    image_with_text = cv2.putText(image, text, position, font, font_scale, font_color, thickness, cv2.LINE_AA)
    cv2.imwrite(output_path, image_with_text)

def main():
    print("Nhấn phím 'S' để bắt đầu, 'E' để thoát...")
    output_path = 'anhvuachup.jpg'
    image_path = 'cropped.jpg'
    running = False
    while True:
        if keyboard.is_pressed("s") and not running:
            print("Starting...")
            capture_image_with_fswebcam(output_path)
            running = True
        elif keyboard.is_pressed("e"):
            break

if __name__ == "__main__":
    main()
