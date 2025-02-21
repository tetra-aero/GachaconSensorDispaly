/* 
# Flight mode button for arduino nano every

## Description:
Main switch           →→ Arduino Nano Every → USB → UART, Serial → Python → PC
Flying mode switch    →↑
Supplying mode switch →↑

## Reference:
1. Arduino Nano Every — Arduino Online Shop
https://store-usa.arduino.cc/products/arduino-nano-every?srsltid=AfmBOopT4m2ACwbTL1XJ0E0ZtFIOGySWbm_JmXyK9p6GdMqJo2xQ0pmp
2. Arduino Nano Every, Pin assignment
https://content.arduino.cc/assets/Pinout-NANOevery_latest.pdf
3. Arduino ボタン Python 連携
https://chatgpt.com/share/67b7bd55-c9ac-800c-bb8b-c0932ccf00a2
*/

#include <Arduino.h>

const int buttonPin = 2;  // ボタンを接続するピン
volatile bool buttonPressed = false;  // 割り込み用のフラグ

const int BuildinLEDPin = 13;  // 基板に実装済みのLED

// 割り込みハンドラ（ISR）
void buttonISR() { 
    buttonPressed = true;
}

void setup() {
    pinMode(BuildinLEDPin, OUTPUT); // LEDを出力モードに設定

    pinMode(buttonPin, INPUT_PULLUP); // 内部プルアップ抵抗を有効化
    Serial.begin(115200);

    // 割り込み設定（FALLING: ボタンが押された瞬間に割り込み発生）
    attachInterrupt(digitalPinToInterrupt(buttonPin), buttonISR, FALLING);
}

void loop() {
    if (buttonPressed) {
        Serial.println("PRESSED"); // Pythonに通知
        buttonPressed = false; // フラグをリセット
        delay(300); // チャタリング対策
    }

    Serial.println("Hello, World!");
    digitalWrite(BuildinLEDPin, HIGH); // LEDを点灯
    delay(500); // 0.5s待つ
    digitalWrite(BuildinLEDPin, LOW); // LEDを消灯
    delay(500); // 0.5s待つ
}
