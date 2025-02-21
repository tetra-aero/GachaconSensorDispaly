/* 
# Flight mode button for arduino nano every

## Description:
Main switch           →→ Arduino Nano Every → USB → UART, Serial → Python → PC
Flying mode switch    →↑
Supplying mode switch →↑

## Reference:
1. Arduino ボタン Python 連携
https://chatgpt.com/share/67b7bd55-c9ac-800c-bb8b-c0932ccf00a2

2. Arduino Nano Every — Arduino Online Shop
https://store-usa.arduino.cc/products/arduino-nano-every?srsltid=AfmBOopT4m2ACwbTL1XJ0E0ZtFIOGySWbm_JmXyK9p6GdMqJo2xQ0pmp
3. Arduino Nano Every, Pin assignment
https://content.arduino.cc/assets/Pinout-NANOevery_latest.pdf

# - SWITCHED_STANDBY_MODE
# - SWITCHED_SUPPLYING_MODE
# - SWITCHED_FLYING_MODE
*/

#include <Arduino.h>

enum State {
    STANDBY_MODE = 0,
    SUPPLYING_MODE,
    FLYING_MODE
};

int current_state = STANDBY_MODE;

const int StandbybuttonPin = 2;   // D2, STANDBYモード（Main switch, 非常停止スイッチ（リモート））のボタンを接続するピン
const int SupplyingbuttonPin = 3; // D3, Suppyingモード（Chargingモード）ボタンを接続するピン
const int FlyingbuttonPin = 4;    // D4, Flyingモードボタンを接続するピン
volatile bool StandbybuttonPressed = false;   // STANDBYモード割り込み用のフラグ
volatile bool SupplyingbuttonPressed = false; // Suppyingモード割り込み用のフラグ
volatile bool FlyingbuttonPressed = false;    // Flyingモード割り込み用のフラグ

const int BuildinLEDPin = 13;  // 基板に実装済みのLED

// STANDBYモード割り込みハンドラ（ISR）
void StandbybuttonISR() { 
    StandbybuttonPressed = true;
}

// Suppyingモード割り込みハンドラ（ISR）
void SupplyingbuttonISR() { 
    SupplyingbuttonPressed = true;
}

// Flyingモード割り込みハンドラ（ISR）
void FlyingbuttonISR() { 
    FlyingbuttonPressed = true;
}

void setup() {
    pinMode(BuildinLEDPin, OUTPUT); // LEDを出力モードに設定

    pinMode(StandbybuttonPin, INPUT_PULLUP);    // 内部プルアップ抵抗を有効化
    pinMode(SupplyingbuttonPin, INPUT_PULLUP);  // 内部プルアップ抵抗を有効化
    pinMode(FlyingbuttonPin, INPUT_PULLUP);     // 内部プルアップ抵抗を有効化

    Serial.begin(115200);

    // STANDBYモード割り込み設定（FALLING: ボタンが押された瞬間に割り込み発生）
    attachInterrupt(digitalPinToInterrupt(StandbybuttonPin), StandbybuttonISR, FALLING);
    // Suppyingモード割り込み設定（FALLING: ボタンが押された瞬間に割り込み発生）
    attachInterrupt(digitalPinToInterrupt(SupplyingbuttonPin), SupplyingbuttonISR, FALLING);
    // Flyingモード割り込み設定（FALLING: ボタンが押された瞬間に割り込み発生）
    attachInterrupt(digitalPinToInterrupt(FlyingbuttonPin), FlyingbuttonISR, FALLING);
}

void loop() {
    // if文の順序により、standby switch > supplying switch > flying switch の順に優先度が高い
    if (StandbybuttonPressed) {
        Serial.print("\n");
        Serial.println("SWITCHED_STANDBY_MODE"); // Pythonに通知
        StandbybuttonPressed = false; // フラグをリセット
        current_state = STANDBY_MODE;
        delay(300); // チャタリング対策
    }
    else if (SupplyingbuttonPressed) {
        Serial.print("\n");
        Serial.println("SWITCHED_SUPPLYING_MODE"); // Pythonに通知
        SupplyingbuttonPressed = false; // フラグをリセット
        current_state = SUPPLYING_MODE;
        delay(300); // チャタリング対策
    }
    else if (FlyingbuttonPressed) {
        Serial.print("\n");  
        Serial.println("SWITCHED_FLYING_MODE"); // Pythonに通知
        FlyingbuttonPressed = false; // フラグをリセット
        current_state = FLYING_MODE;
        delay(300); // チャタリング対策
    }
    else {
        // 何もしない
    }

    Serial.print(".");
    digitalWrite(BuildinLEDPin, HIGH); // LEDを点灯
    delay(100); // 0.1s待つ
    digitalWrite(BuildinLEDPin, LOW); // LEDを消灯
    delay(100); // 0.1s待つ
}
