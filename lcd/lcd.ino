#include <LiquidCrystal_I2C.h>
#include <Wire.h> 
#define MAX_SPACES 5 // Số lượng ô trống tối đa hiển thị trên LCD

int spaceArray[MAX_SPACES]; // Mảng lưu trữ số thứ tự của các ô trống
bool spaceChanged = false; // Biến đánh dấu xem trạng thái của ô trống đã thay đổi hay không
bool lastSpaceState[MAX_SPACES]; // Mảng lưu trữ trạng thái của các ô trống ở lần cập nhật trước
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Khai báo kết nối LCD I2C (địa chỉ 0x27, kích thước 16x2)
int dataReceived;

unsigned long lastUpdateTime = 0; // Thời điểm cập nhật dữ liệu cuối cùng
unsigned long updateInterval = 1000; // Khoảng thời gian cập nhật (ms)

void setup() {
  Serial.begin(9600);  // Khởi động cổng serial
  lcd.init();           // Khởi động màn hình LCD
  lcd.backlight();      // Bật đèn nền LCD
}

void loop() {
  if (Serial.available() > 0) {
    String dataReceived = Serial.readStringUntil('\n'); // Đọc dữ liệu từ cổng serial
    if (millis() - lastUpdateTime >= updateInterval) {
      displaySpaceNumbers(dataReceived); // Hiển thị các số thứ tự lên LCD nếu đến thời điểm cập nhật
      lastUpdateTime = millis(); // Cập nhật thời điểm cập nhật cuối cùng
    }
  }
}

void displaySpaceNumbers(String data) {
  lcd.clear();               // Xóa màn hình LCD
  lcd.setCursor(0, 0);       // Đặt con trỏ ở hàng đầu tiên
  lcd.print("Empty Spaces: "); // Hiển thị tiêu đề
  
  // Phân tích chuỗi nhận được và lưu vào mảng
  int i = 0;
  while (data.length() > 0 && i < MAX_SPACES) {
    int commaIndex = data.indexOf(',');
    if (commaIndex != -1) {
      spaceArray[i] = data.substring(0, commaIndex).toInt();
      data = data.substring(commaIndex + 1);
    } else {
      spaceArray[i] = data.toInt();
      data = "";
    }
    i++;
  }

  // So sánh trạng thái của ô trống với lần cập nhật trước
  for (int j = 0; j < i; j++) {
    if (spaceArray[j] != lastSpaceState[j]) {
      spaceChanged = true;
      break;
    }
  }

  // Nếu trạng thái của ô trống đã thay đổi, hiển thị lại trên LCD và cập nhật lại trạng thái
  if (spaceChanged) {
    lcd.setCursor(0, 1); // Đặt con trỏ ở dòng thứ hai
    for (int j = 0; j < i; j++) {
      lcd.print(spaceArray[j]);
      lcd.print(" ");
      lastSpaceState[j] = spaceArray[j]; // Cập nhật lại trạng thái của ô trống
    }
    spaceChanged = false; // Đánh dấu rằng dữ liệu đã được cập nhật
  }
}