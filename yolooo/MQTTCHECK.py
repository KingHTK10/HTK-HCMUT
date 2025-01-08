import random
import cv2
import time
import numpy as np
from ultralytics import YOLO
import paho.mqtt.client as mqtt

# Xác định tọa độ của ô 1
parking_spot_x_min = 287
parking_spot_x_max = 345
parking_spot_y_min = 195
parking_spot_y_max = 324
# slot ô 2
parking_spot_x_min1 = 346
parking_spot_x_max1 = 405
parking_spot_y_min1 = 195
parking_spot_y_max1 = 320

# opening the file in read mode
my_file = open("utils/coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
my_file.close()

mqtt_server = "d0f56a6d14c34667b8a4d2107a735edc.s1.eu.hivemq.cloud"
PORT = 8883
mqtt_username = "htkiet10"
mqtt_password = "Htk14042002ZXC"
TOPIC = "mqttHQ-client-test"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect to MQTT broker")

client = mqtt.Client()
client.on_connect = on_connect

print("Connecting to MQTT broker...")
client.connect(mqtt_server, PORT)
client.loop_start()

# Generate random colors for class list
detection_colors = []
for i in range(len(class_list)):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    detection_colors.append((b, g, r))

# load a pretrained YOLOv8n model\
model = YOLO("runs/detect/train10/train6/weights/best.pt", "v8",)

# Open video file
cap = cv2.VideoCapture("car1.mp4")

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Predict on image
    detect_params = model.predict(source=[frame], save=False, conf=0.4)
    # Kiểm tra và cập nhật trạng thái của việc nhận diện
    detected_wrong_parking = False
    if len(detect_params[0]) != 0:
        detected_wrong_parking = True
        if detected_wrong_parking:
            for i in range(len(detect_params[0])):
                boxes = detect_params[0].boxes
                box = boxes[i]
                bb = box.xyxy.numpy()[0]
                x_min, y_min, x_max, y_max = int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])
                x_center = (x_min + x_max)/2
                y_center = (y_min + y_max) / 2
                # Kiểm tra xem tọa độ của bounding box có trùng với ô đậu không
                if parking_spot_x_min < x_min < parking_spot_x_max and parking_spot_y_min < y_min < parking_spot_y_max or parking_spot_x_min < x_max < parking_spot_x_max and parking_spot_y_min < y_max < parking_spot_y_max:
                    client.publish(TOPIC, str(int(1)))
                    print("xe chạm ô 1 ")
                if parking_spot_x_min1 < x_min < parking_spot_x_max1 and parking_spot_y_min1 < y_min < parking_spot_y_max1 or parking_spot_x_min1 < x_max < parking_spot_x_max1 and parking_spot_y_min1 < y_max < parking_spot_y_max1:
                    client.publish(TOPIC, str(int(2)))
                    print("xe chạm ô 2")
                #if parking_spot_x_min2 < x_min < parking_spot_x_max2 and parking_spot_y_min2 < y_min < parking_spot_y_max2 or parking_spot_x_min2 < x_max < parking_spot_x_max2 and parking_spot_y_min2 < y_max < parking_spot_y_max2:
                    #client.publish(TOPIC, str(int(3)))
                    #print("xe chạm ô 3")
                #if parking_spot_x_min3 < x_center < parking_spot_x_max3 or parking_spot_x_min3 < x_center < parking_spot_x_max3 and parking_spot_y_min3 < y_center < parking_spot_y_max3:
                    #client.publish(TOPIC, str(int(4)))
                    #print("xe chạm ô 3")

    # Hiển thị kết quả nhận diện trên frame
    if len(detect_params[0]) != 0:
        for i in range(len(detect_params[0])):
            boxes = detect_params[0].boxes
            box = boxes[i]  # returns one box
            clsID = box.cls.numpy()[0]

            # Chỉ xử lý bounding box cho lớp thứ 80
            if clsID == 80:
                conf = box.conf.numpy()[0]
                bb = box.xyxy.numpy()[0]

                cv2.rectangle(
                    frame,
                    (int(bb[0]), int(bb[1])),
                    (int(bb[2]), int(bb[3])),
                    detection_colors[int(clsID)],
                    3,
                )

                # Hiển thị tên lớp và độ tin cậy
                font = cv2.FONT_HERSHEY_COMPLEX
                cv2.putText(
                    frame,
                    class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    1,
                    (255, 255, 255),
                    2,
                )

    # Hiển thị frame kết quả
    cv2.imshow("ObjectDetection", frame)

    # Kết thúc chương trình khi nhấn phím "Q"
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()