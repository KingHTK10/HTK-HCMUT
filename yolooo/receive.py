import json
import paho.mqtt.client as mqtt

# MQTT broker configuration
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "car_park"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect to MQTT broker")

def on_message(client, userdata, msg):
    car_park_status_bytes = msg.payload
    car_park_status_str = car_park_status_bytes.decode('utf-8')  # Decode từ dạng bytes sang chuỗi
    car_park_status = json.loads(car_park_status_str)
    if car_park_status == 1:
        print("Car parked in the wrong spot 1!")
    elif car_park_status == 2:
        print("cars parked in the wrong spot 2 ")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to MQTT broker...")
client.connect(BROKER, PORT)
client.loop_forever()
