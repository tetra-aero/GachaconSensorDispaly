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

#define Version "1.0"

enum State {
    EMERGENCY_MODE = -1,
    STANDBY_MODE = 0,
    SUPPLYING_MODE,
    FLYING_MODE
};

int current_state = STANDBY_MODE;

const int EmergencybuttonPin = 2;   // D2, Emergencyモード（Main switch, 非常停止スイッチ（リモート））のボタンを接続するピン
const int SupplyingbuttonPin = 3; // D3, Suppyingモード（Chargingモード）ボタンを接続するピン
const int FlyingbuttonPin = 4;    // D4, Flyingモードボタンを接続するピン
volatile bool EmergencybuttonSwitched = false;   // Emergencyモード割り込み用のフラグ
volatile bool SupplyingbuttonSwitched = false; // Suppyingモード割り込み用のフラグ
volatile bool FlyingbuttonSwitched = false;    // Flyingモード割り込み用のフラグ

const int BuildinLEDPin = 13;  // 基板に実装済みのLED

int period_count = 0;
int period = 20; // 20 * 0.1s = 2s

int EmergencybuttonState;     // Emergencyモードボタンの状態を取得
int SupplyingbuttonState; // Suppyingモードボタンの状態を取得
int FlyingbuttonState;       // Flyingモードボタンの状態を取得

// Emergencyモード割り込みハンドラ（ISR）
void EmergencybuttonISR() { 
    EmergencybuttonSwitched = true;
}

// Suppyingモード割り込みハンドラ（ISR）
void SupplyingbuttonISR() { 
    SupplyingbuttonSwitched = true;
}

// Flyingモード割り込みハンドラ（ISR）
void FlyingbuttonISR() { 
    FlyingbuttonSwitched = true;
}

void setup() {
    pinMode(BuildinLEDPin, OUTPUT); // LEDを出力モードに設定

    pinMode(EmergencybuttonPin, INPUT_PULLUP);    // 内部プルアップ抵抗を有効化
    pinMode(SupplyingbuttonPin, INPUT_PULLUP);  // 内部プルアップ抵抗を有効化
    pinMode(FlyingbuttonPin, INPUT_PULLUP);     // 内部プルアップ抵抗を有効化

    Serial.begin(115200);

    EmergencybuttonState = digitalRead(EmergencybuttonPin);     // Emergencyモードボタンの状態を取得
    SupplyingbuttonState = digitalRead(SupplyingbuttonPin); // Suppyingモードボタンの状態を取得
    FlyingbuttonState = digitalRead(FlyingbuttonPin);       // Flyingモードボタンの状態を取得

    // STANDYモード割り込み設定（CHANGE: ボタンが押された瞬間に割り込み発生）
    attachInterrupt(digitalPinToInterrupt(EmergencybuttonPin), EmergencybuttonISR, CHANGE);
    // Suppyingモード割り込み設定（CHANGE: ボタンが押された瞬間に割り込み発生）
    attachInterrupt(digitalPinToInterrupt(SupplyingbuttonPin), SupplyingbuttonISR, CHANGE);
    // Flyingモード割り込み設定（CHANGE: ボタンが押された瞬間に割り込み発生）
    attachInterrupt(digitalPinToInterrupt(FlyingbuttonPin), FlyingbuttonISR, CHANGE);

}

void loop() {
    EmergencybuttonState = digitalRead(EmergencybuttonPin);     // Emergencyモードボタンの状態を取得
    SupplyingbuttonState = digitalRead(SupplyingbuttonPin); // Suppyingモードボタンの状態を取得
    FlyingbuttonState = digitalRead(FlyingbuttonPin);       // Flyingモードボタンの状態を取得

    // if文の順序により、standby switch > supplying switch > flying switch の順に優先度が高い
    // チャタリング回避で、後にあるdelay(100)*2で、0.2sごとに判断する
    if (EmergencybuttonSwitched) {
      Serial.print("\n");
      Serial.println("SWITCHED_EMERGENCY_MODE_BUTTON");
        if (EmergencybuttonState == LOW) { // active low
            Serial.println("SWITCHED_EMERGENCY_MODE"); // Pythonに通知
            current_state = EMERGENCY_MODE;
        }
        else {  //EmergencybuttonState == LOW // active low
            Serial.println("SWITCHED_STANDBY_MODE"); // Pythonに通知
            current_state = STANDBY_MODE;
        }
        EmergencybuttonSwitched = false; // フラグをリセット
    }
    else if (SupplyingbuttonSwitched) {
      if (current_state == STANDBY_MODE) {
          Serial.print("\n");
          Serial.println("SWITCHED_SUPPLYING_MODE_BUTTON");
          if (SupplyingbuttonState == LOW) { // active low
              Serial.println("SWITCHED_SUPPLYING_MODE"); // Pythonに通知
              current_state = SUPPLYING_MODE;
          }
          else {  //SupplyingbuttonState == HIGH
              // Standby modeに戻る
              Serial.println("SWITCHED_STANDBY_MODE"); // Pythonに通知
              current_state = STANDBY_MODE;
          }
      }
      else { // from SUPPLYING_MODE or FLYING_MODE or EMERGENCY_MODE
          // 何もしない
      }
      SupplyingbuttonSwitched = false; // フラグをリセット
    }
    else if (FlyingbuttonSwitched) {
      if (current_state == STANDBY_MODE) {
          Serial.print("\n");
          Serial.println("SWITCHED_FLYING_MODE_BUTTON");
          if (FlyingbuttonState == LOW) { // active low
              Serial.print("\n");  
              Serial.println("SWITCHED_FLYING_MODE"); // Pythonに通知
              current_state = FLYING_MODE;
          }
          else {  //FlyingbuttonState == HIGH
              // Standby modeに戻る
              Serial.print("\n");
              Serial.println("SWITCHED_STANDBY_MODE"); // Pythonに通知
              current_state = STANDBY_MODE;
          }
      }
      else { // from SUPPLYING_MODE or FLYING_MODE or EMERGENCY_MODE
          // 何もしない
      }
      FlyingbuttonSwitched = false; // フラグをリセット
    }
    else {
        // 何もしない
    }

    Serial.print(".");
    digitalWrite(BuildinLEDPin, HIGH); // LEDを点灯
    delay(100); // 0.1s待つ
    digitalWrite(BuildinLEDPin, LOW); // LEDを消灯
    delay(100); // 0.1s待つ

    // 2sごとに状態をserialで送る
    period_count = period_count + 2;
    if (period_count >= period) {
        period_count = 0;
        if (current_state == STANDBY_MODE) {
            Serial.print("\n");
            Serial.println("CURRENT_STANDBY_MODE");
        }
        else if (current_state == SUPPLYING_MODE) {
            Serial.print("\n");
            Serial.println("CURRENT_SUPPLYING_MODE");
        }
        else if (current_state == FLYING_MODE) {
            Serial.print("\n");
            Serial.println("CURRENT_FLYING_MODE");
        }
        else {  // current_state == EMERGENCY_MODE)
            Serial.print("\n");
            Serial.println("CURRENT_EMERGENCY_MODE");
        }
    }
}
