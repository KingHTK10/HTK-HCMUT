#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi and MQTT broker configuration
const char* ssid = "10";
const char* password = "14042002";
const char* mqtt_server = "public.mqtthq.com";
const int mqttPort = 1883;
const char* mqttTopic = "mqttHQ-client-test";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

const int ledPin1 = D0;
const int ledPin2 = D1;
const int ledPin3 = D2;
const int ledPin4 = D3;
const int ledPin5 = D4;

const int maxDataSize = 10;
int data[maxDataSize];
int dataSize = 0;
unsigned long lastDataReceivedTime = 0;

void setupled() {
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin4, OUTPUT);
  pinMode(ledPin5, OUTPUT);
}

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  mqttClient.setServer(mqtt_server, mqttPort);
  mqttClient.setCallback(onMqttMessage);

  while (!mqttClient.connected()) {
    if (mqttClient.connect("NodeMCUClient")) {
      Serial.println("Connected to MQTT broker");
      mqttClient.subscribe(mqttTopic);
    } else {
      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }

  setupled();
}

void loop() {
  mqttClient.loop();

  if (millis() - lastDataReceivedTime > 5000) {
    turnOffAllLEDs();
  }
}

void turnOffAllLEDs() {
  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(ledPin3, LOW);
  digitalWrite(ledPin4, LOW);
  digitalWrite(ledPin5, LOW);
}

void onMqttMessage(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0';
  int value = atoi((char*)payload);
  Serial.print("Received message: ");
  Serial.println(value);

  if (dataSize < maxDataSize) {
    data[dataSize] = value;
    dataSize++;
    lastDataReceivedTime = millis();

    if (dataSize == maxDataSize) {
      controlLEDs();
      dataSize = 0;
    }
  }
}

void controlLEDs() {
  bool led1 = false;
  bool led2 = false;
  bool led3 = false;
  bool led4 = false;
  bool led5 = false;

  for (int i = 0; i < maxDataSize; i++) {
    int value = data[i];

    if (value == 1) {
      led1 = true;
    } else if (value == 2) {
      led2 = true;
    } else if (value == 3) {
      led3 = true;
    } else if (value == 4) {
      led4 = true;
    } else if (value == 5) {
      led5 = true;
    }
  }

  digitalWrite(ledPin1, led1 ? HIGH : LOW);
  digitalWrite(ledPin2, led2 ? HIGH : LOW);
  digitalWrite(ledPin3, led3 ? HIGH : LOW);
  digitalWrite(ledPin4, led4 ? HIGH : LOW);
  digitalWrite(ledPin5, led5 ? HIGH : LOW);
}