import cv2

# Đọc ảnh gốc
image = cv2.imread("img_4.png", cv2.IMREAD_GRAYSCALE)

# Áp dụng phép làm mờ Gauss để giảm nhiễu
blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Áp dụng phép ngưỡng nhị phân
_, binary_image = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

# Hiển thị ảnh gốc và ảnh nhị phân
cv2.imshow("Original Image", image)
cv2.imshow("Binary Image", binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
