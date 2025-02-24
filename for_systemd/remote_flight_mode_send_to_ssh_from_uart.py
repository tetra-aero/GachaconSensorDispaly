# remote_flight_mode_send_to_ssh_from_uart.py
#
# Reference 1, Arduino ボタン Python 連携
# https://chatgpt.com/share/67b7bd55-c9ac-800c-bb8b-c0932ccf00a2
#
# - SWITCHED_EMERGENCY_MODE
# - SWITCHED_STANDBY_MODE
# - SWITCHED_SUPPLYING_MODE
# - SWITCHED_FLYING_MODE
#
# CURRENT_STANDBY_MODE
# CURRENT_SUPPLYING_MODE
# CURRENT_FLYING_MODE
# CURRENT_EMERGENCY_MODE
#
# > ModuleNotFoundError: No module named 'serial'
# python -m pip install pyserial
#
# Reference 2, Ubuntu 20.04 の Arduino IDE で ESP32 Dev Moduleを使ってコンパイルする際にpythonが無いと怒られる #ubuntu20.04 - Qiita
# https://qiita.com/ketaro-m/items/edd40ba08ff61c7bc0e6
#

import serial
import subprocess
from enum import Enum
import datetime

# Arduinoのシリアルポートを指定（適宜変更）
SERIAL_PORT = "/dev/ttyACM0"  # Windowsなら "COM3" などに変更
BAUD_RATE = 115200

class State(Enum):
    STANDBY_MODE = 0
    SUPPLYING_MODE = 1
    FLYING_MODE = 2
    EMERGENCY_MODE = -1

current_state = State.STANDBY_MODE


try:
    # シリアルポートを開く
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Serial connected to {SERIAL_PORT}")

    while True:
        # シリアルデータを受信
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").strip()
            if line == "SWITCHED_STANDBY_MODE":
                print("STANDBY_MODE, execute standby mode script...")
                subprocess.run(["python", "test_paramiko_cansend_mode_standby.py"])  # 外部スクリプト実行
                current_state = State.STANDBY_MODE
            elif line == "SWITCHED_SUPPLYING_MODE":
                None
            elif line == "SWITCHED_FLYING_MODE":
                None
            elif line == "SWITCHED_EMERGENCY_MODE":
                print("EMERGENCY_MODE, execute emergency mode script...")
                subprocess.run(["python", "test_paramiko_cansend_mode_standby.py"])  # 外部スクリプト実行
                current_state = State.EMERGENCY_MODE
            elif line == "CURRENT_STANDBY_MODE":
                if current_state != State.STANDBY_MODE:
                    print("STANDBY_MODE, execute standby mode script...")
                    subprocess.run(["python", "test_paramiko_cansend_mode_standby.py"])
                current_state = State.STANDBY_MODE
            elif line == "CURRENT_SUPPLYING_MODE":
                if current_state != State.SUPPLYING_MODE:
                    print("SUPPLYING_MODE, execute supplying mode script...")
                    subprocess.run(["python", "test_paramiko_cansend_mode_supplying.py"])  # 外部スクリプト実行
                current_state = State.SUPPLYING_MODE
            elif line == "CURRENT_FLYING_MODE":
                if current_state != State.FLYING_MODE:
                    print("FLYING_MODE, execute flying mode script...")
                    subprocess.run(["python", "test_paramiko_cansend_mode_flying.py"])  # 外部スクリプト実行
                current_state = State.FLYING_MODE
            elif line == "CURRENT_EMERGENCY_MODE":
                if current_state != State.EMERGENCY_MODE:
                    print("EMERGENCY_MODE, execute emergency mode script...")
                    subprocess.run(["python", "test_paramiko_cansend_mode_standby.py"])
                current_state = State.EMERGENCY_MODE
            else:
                None
            #pass
            #print(".", end="")
            #print(line)
            #if line in ".":
            print("CURRENT_STATE: " + current_state.name + ", " + datetime.datetime.now().isoformat())
            #pass
        #pass
    #pass

except serial.SerialException as e:
    print(f"シリアルポートエラー: {e}")
except KeyboardInterrupt:
    print("終了")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("シリアルポートを閉じました")
    #pass
#pass

# End of file
