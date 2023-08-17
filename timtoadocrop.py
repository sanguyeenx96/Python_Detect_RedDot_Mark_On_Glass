import cv2

# Biến toàn cục lưu trữ thông tin vùng cắt
x_start, y_start, x_end, y_end = 0, 0, 0, 0
drawing = False

def draw_rectangle(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start = x, y
        drawing = True
    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        drawing = False
        print(f"x: {x_start}, y: {y_start}, w: {x_end - x_start}, h: {y_end - y_start}")

# Tạo cửa sổ và đọc ảnh
image = cv2.imread('cropped.jpg')
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_rectangle)

while True:
    if drawing:
        temp_image = image.copy()
        cv2.rectangle(temp_image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow('Image', temp_image)
    else:
        cv2.imshow('Image', image)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
