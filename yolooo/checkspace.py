import cv2
import pickle
import serial
import time
import numpy as np
import cvzone

# Khởi tạo kết nối serial với Arduino
#ser = serial.Serial('COM7', 9600)
time.sleep(2)  # Đợi 2 giây để Arduino khởi động

cap = cv2.VideoCapture("carPark.mp4")
width, height = 103, 50
#width, height = 50,50
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


def empty(a):
    pass

cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 240)
cv2.createTrackbar("Val1", "Vals", 20, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)


def checkSpaces():

    empty_spaces = []
    spaces = 0
    space_number = 1
    for space_number, pos in enumerate(posList, start=1):  # Bắt đầu từ số 1
        x, y = pos
        w, h = width, height

        imgCrop = imgThres[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)
        #cv2.imshow(str(x*y), imgCrop)
        if count < 950:
            empty_spaces.append(space_number)

        if count < 950:
            color = (0, 200, 0)
            thic = 5
            spaces += 1
        else:
            color = (0, 0, 200)
            thic = 2

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)
        cv2.putText(img, str(space_number), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)  # Hiển thị số thứ tự của ô đậu xe

        space_number += 1

    cvzone.putTextRect(img, f'Free: {spaces}/{len(posList)}', (50, 60), thickness=3, offset=20, colorR=(0, 200, 0))

    if empty_spaces:
        print("Các ô trống:")
        for space_num in empty_spaces:
            print("Ô số:", space_num)

        # Gửi số thứ tự của các ô trống asang Arduino
        data_to_send = ','.join(map(str, empty_spaces)) + '\n'  # Chuyển danh sách thành chuỗi và gửi đi
        #ser.write(data_to_send.encode())

    else:
        print("Không có ô trống.")


#print("Kích thước video:", int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), "x", int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Xử lý khi nhấn phím 'r' để reset
def handle_key_press(key):
    if key == ord('r'):
        pass  # Thực hiện các thao tác reset ở đây


# Bắt đầu vòng lặp chính
while True:
    # Lấy khung hình từ video
    ret, img = cap.read()
    if not ret:  # Kiểm tra xem đã đến cuối video chưa
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Quay lại vị trí đầu tiên
        continue  # Tiếp tục vòng lặp để đọc khung hình mới

    # Chuyển đổi sang ảnh xám và làm mờ
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    # Xử lý ngưỡng và làm mờ để làm sạch ảnh
    val1 = cv2.getTrackbarPos("Val1", "Vals") # Adaptive Thresholding để xác định kích thước cửa sổ lân cận cho việc tính toán ngưỡng
    val2 = cv2.getTrackbarPos("Val2", "Vals") # Adaptive Thresholding để điều chỉnh ngưỡng cho việc chuyển đổi ảnh màu sang ảnh đen trắng
    val3 = cv2.getTrackbarPos("Val3", "Vals") # Median Blur để điều chỉnh kích thước của kernel màu xám
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1
    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)

    # Check các ô trống và gửi dữ liệu sang Arduino
    checkSpaces()

    # Hiển thị các khung hình đầu ra
    cv2.imshow("Image", img)
    cv2.imshow("ImageGray", imgThres)
    cv2.imshow("ImageBlur", imgBlur)

    # Xử lý sự kiện phím
    key = cv2.waitKey(1)
    if key != -1:
        handle_key_press(key)

