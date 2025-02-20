#include <Arduino.h>

const int buttonPin = 2;  // ボタンを接続するピン
volatile bool buttonPressed = false;  // 割り込み用のフラグ

// 割り込みハンドラ（ISR）
void buttonISR() { 
    buttonPressed = true;
}

void setup() {
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
}
