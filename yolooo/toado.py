import cv2


# Hàm callback được gọi khi chuột được click
def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Tọa độ pixel: ({x}, {y})")


def get_pixel_coordinates(video_path):
    # Mở video
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Không thể mở video.")
        return

    # Tạo cửa sổ để hiển thị video
    cv2.namedWindow("Video")

    # Thiết lập callback cho sự kiện chuột
    cv2.setMouseCallback("Video", mouse_callback)

    # Lặp qua từng frame trong video
    while True:
        ret, frame = cap.read()

        # Kiểm tra nếu đọc frame thành công
        if ret:
            # Hiển thị frame
            cv2.imshow("Video", frame)

            # Đợi bất kỳ phím nào được nhấn trong 1ms
            key = cv2.waitKey(1) & 0xFF

            # Nếu nhấn phím 'q', thoát vòng lặp
            if key == ord('q'):
                break
        else:
            break

    # Giải phóng tài nguyên
    cap.release()
    cv2.destroyAllWindows()


# Đường dẫn đến video
video_path = "car1.mp4"

# Gọi hàm để lấy tọa độ pixel khi click chuột
get_pixel_coordinates(video_path)
