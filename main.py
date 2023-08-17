import cv2
import numpy as np
import tkinter as tk
import subprocess
import time

def button_clicked():
    status_label.config(text="TAKING PICTURE", bg="black",fg="orange",font=("Helvetica",50))
    root.update_idletasks()
    capture_image_with_fswebcam()


def capture_image_with_fswebcam():
    try:
        start_time = time.time()
        subprocess.run(['fswebcam', '-r', '1600x1200', '--no-banner', '--jpeg','95','-F','8', 'anhvuachup.jpg'])
        #subprocess.run(['fswebcam', '-r', '1600x1200', '--no-banner', '--fps','60','-F','5', 'anhvuachup.jpg'])

        status_label.config(text="TAKED PICTURE",font=("Helvetica",50))
        root.update_idletasks()
        print(f"Ảnh đã được chụp và lưu")
        end_time = time.time()
        timecount = end_time - start_time
        print("Thoi gian check", timecount)

        crop_image(input_path='anhvuachup.jpg', output_path='cropped.jpg',x=500,y=450,w=450,h=144)

    except Exception as e:
        print("Có lỗi xảy ra:", e)
        status_label.config(text="CAN'T TAKE PICTURE",bg="red",font=("Helvetica",50))
        root.update_idletasks()
def crop_image(input_path, output_path, x,y,w,h):
    try:
        status_label.config(text="CROPING AREA",font=("Helvetica",50))
        root.update_idletasks()
        image = cv2.imread(input_path)
        cropped_image = image[y:y+h,x:x+w]
        cv2.imwrite(output_path,cropped_image)
        status_label.config(text="CROPED AREA",font=("Helvetica",50))
        root.update_idletasks()        
        print("Anh da duoc cat va luu lai", output_path)
        checking()
    except Exception as e:
        print("Co loi xay ra", e)
def checking():
    status_label.config(text="CHECKING",font=("Helvetica",50))
    root.update_idletasks()
    image = cv2.imread('cropped.jpg')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100,85])
    upper_red = np.array([10, 255, 255])
    print("bat dau check")
    try:
        mask = cv2.inRange(hsv, lower_red, upper_red)
        red_sum =np.sum(image[mask > 0,2])
        print(int(red_sum))
        giatri = int(red_sum)
        if giatri > 60:
            status_label.config(text="OK", bg="green",fg="white",font=("Helvetica",50))
            root.update_idletasks()
            cv2.imshow("1",image)
            cv2.imshow("2",hsv)
            cv2.imshow("3",mask)
            cv2.waitKey()

        else:
            status_label.config(text="NG", bg="red",fg="white",font=("Helvetica",50))
            root.update_idletasks()
            cv2.imshow("1",image)
            cv2.imshow("2",hsv)
            cv2.imshow("3",mask)
            cv2.waitKey()

    except:
        print("NG")
        status_label.config(text="Khong chup duoc anh", bg="red",fg="white",font=("Helvetica",50))
        root.update_idletasks()

root = tk.Tk()
root.title("Raspberry Pi")
root.geometry("800x600")
button = tk.Button(root, text="Start check", bg="green", fg="white", command=button_clicked)
button.pack(pady=20,fill="x")

status_label = tk.Label(root, text="READY", bg="black",fg="orange", font=("Helvetica",150),height="300")
status_label.pack(pady=20,fill="x")

root.mainloop()
