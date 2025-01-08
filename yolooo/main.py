import random
import cv2
import numpy as np
from ultralytics import YOLO
import paho.mqtt.client as mqtt

# Đọc danh sách các lớp từ tệp
with open("utils/coco.txt", "r") as f:
    class_list = f.read().split("\n")

# Thiết lập MQTT
#mqtt_server = "public.mqtthq.com"
#PORT = 1883
#TOPIC = "mqttHQ-client-test"

#def on_connect(client, userdata, flags, rc):
    #if rc == 0:
        #print("Connected to MQTT broker")
    #else:
        #print("Failed to connect to MQTT broker")

#client = mqtt.Client()
#client.on_connect = on_connect

#print("Connecting to MQTT broker...")
#client.connect(mqtt_server, PORT)
#client.loop_start()

# Tạo màu ngẫu nhiên cho các lớp
detection_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(len(class_list))]

# Load mô hình YOLO
model = YOLO("runs/detect/train5 (2)/train5/weights/best.pt", "v8")

# Mở video
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Dự đoán trên frame
    detect_params = model.predict(source=[frame], save=False)

    parking_spots = []
    cars = []

    # Phân loại bounding box cho ô đỗ xe và xe
    for box in detect_params[0].boxes:
        clsID = int(box.cls.numpy()[0])
        bb = box.xyxy.numpy()[0]

        if clsID == 81:  # Lớp ô đỗ xe (đảm bảo rằng 81 là chỉ số đúng của lớp ô đỗ xe)
            parking_spots.append(bb)
        elif clsID == 80:  # Lớp xe (đảm bảo rằng 80 là chỉ số đúng của lớp xe)
            cars.append(bb)

    # Sắp xếp các ô xe theo tọa độ x
    parking_spots.sort(key=lambda x: x[0])

    # Gán số thứ tự cho các ô xe và hiển thị lên frame
    for idx, spot_bb in enumerate(parking_spots, start=1):
        s_x_min, s_y_min, s_x_max, s_y_max = spot_bb
        cv2.putText(frame, f"{idx}", (int((s_x_min + s_x_max) / 2), int((s_y_min + s_y_max) / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Kiểm tra tọa độ của các ô đậu xe so với tọa độ của các ô xe
    for car_bb in cars:
        for spot_idx, spot_bb in enumerate(parking_spots, start=1):
            s_x_min, s_y_min, s_x_max, s_y_max = spot_bb

            # Kiểm tra xem tọa độ của chiếc xe có nằm trong bounding box của ô đậu xe không
            if (s_x_min < car_bb[0] < s_x_max and s_y_min < car_bb[1] < s_y_max) or (s_x_min < car_bb[2] < s_x_max and s_y_min < car_bb[3] < s_y_max):
                #client.publish(TOPIC, str(spot_idx))
                print("xe chạm ô " f"{spot_idx}")
                # break  # Dừng vòng lặp nếu đã tìm thấy ô đậu tương ứng

    # Hiển thị bounding box và nhãn
    for box in detect_params[0].boxes:
        clsID = int(box.cls.numpy()[0])
        conf = box.conf.numpy()[0]
        bb = box.xyxy.numpy()[0]

        cv2.rectangle(frame, (int(bb[0]), int(bb[1])), (int(bb[2]), int(bb[3])), detection_colors[clsID], 3)

        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, class_list[clsID] + " " + str(round(conf, 3)) + "%", (int(bb[0]), int(bb[1]) - 10), font, 1, (255, 255, 255), 2)

    # Hiển thị frame kết quả
    cv2.imshow("ObjectDetection", frame)

    # Kết thúc chương trình khi nhấn phím "Q"
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
