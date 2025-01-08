import cv2
import os

# Đường dẫn đến thư mục chứa ảnh
folder_path = "F:\\yolo\\oxe"

# Lặp qua tất cả các tệp tin trong thư mục
for filename in os.listdir(folder_path):
    # Kiểm tra tệp tin có phải là ảnh không
    if filename.endswith((".jpg", ".jpeg", ".png")):
        # Đường dẫn đầy đủ của ảnh
        image_path = os.path.join(folder_path, filename)

        # Đọc ảnh
        image = cv2.imread(image_path)

        # Resize ảnh về kích thước 640x640
        resized_image = cv2.resize(image, (640, 640))

        # Lưu ảnh mới với cùng tên và định dạng
        cv2.imwrite(image_path, resized_image)