import json
from pathlib import Path
import datetime
import time
import requests
import can
from datetime import datetime, timedelta
from enum import Enum

class State(Enum):
    Standby                      = 0
    Supplying_Precharge         = 1
    Supplying_Intermediate      = 2
    Supplying                   = 3
    Flying_Supply_Precharge     = 4
    Flying_Supply_Intermediate  = 5
    Flying_Supply_only          = 6
    Flying_ESC_Precharge        = 7
    Flying_ESC_Intermediate     = 8
    Flying                      = 9
    Discharge_Precharge         = 10
    Discharge_Intermediate      = 11
    Discharge                   = 12
    Manual                      = 90 #0x5A

Current_state = State.Standby
jdata = {}

#can_bus = can.interface.Bus(channel="can0", interface='socketcan')
can_bus = can.interface.Bus(channel="vcan0", interface='socketcan')
#previous_time = datetime.now()
previous_time = int(time.time()*1000)

number_of_devices = 0x23
number_of_element = number_of_devices*4

outjson = [0 for _ in range(number_of_element)]
outjson_old = [0 for _ in range(number_of_element)]

outjson_list                    = []
outjson_list_old                = []
outjson_list_0x1300_voltage     = []
outjson_list_0x2000_throttle    = []
outjson_list_0x2200_current     = []
outjson_list_0x2500_lv_voltage  = []
outjson_list_0x6000_mode        = []

Wait_seconds_Supply_Relay_Precharge = 7
Count_seconds_Supply_Relay_Precharge = 0

Wait_seconds_Motor_Relay_Precharge = 7
Count_seconds_Motor_Relay_Precharge = 0

temp_lv_bat_vol = 0.0

while 1:
    #current_time = datetime.now()  # 現在の時刻を取得
    current_time = int(time.time()*1000)  # 現在の時刻を取得  # 現在の時刻を取得 100/1000ms毎に精度アップ
    msg = can_bus.recv(0.1)  # 0.1秒待機してメッセージを受信
    if msg:
        #print (msg)
        #print(msg.channel)
        #print(format(msg.arbitration_id, '02X'))
        tmp = ""
        for i in range(msg.dlc):
            tmp = tmp + format(msg.data[i], '02X') + " "
        tmp = tmp[:-1]
        #print(tmp)
        jdata["0x" +format(msg.arbitration_id, '04X')] = tmp
    else:
        #print("No message")
        pass

    #=========================================================================#
    ## 1秒おきに実行 → 100ms毎に実行
    #=========================================================================#
    #if current_time.second != previous_time.second:
    if current_time - previous_time > 100: #defferent 100ms judge
        gap_time = current_time - previous_time
        gap_msg = "Interval:" + str(gap_time) +"ms"
        print(gap_msg)
        #print(jdata)
        for i in range(number_of_devices):
            try:
            #--------------------------------------------------------------------------#
                if f"0x{(0x1300 + i):04X}" in jdata:
                    # 0x1300, voltage, uint16_t bus_voltage; バス電圧, 0.1V
                    strdata = jdata[(f"0x{(0x1300 + i):04X}")].split()
                    data = (int(strdata[1], 16)<<8 | int(strdata[0], 16))
                    object_data = {}
                    object_data["title"] = "HV Bus Voltage No." + str(i)
                    object_data["data"] = round( (data/10.0) ,1)
                    object_data["raw"] = ("0x"+format(data, '04X'))
                    object_data["unit"] = " V"
                    #print(object_data)
                    #outjson.append(object_data)
                    outjson[number_of_devices*0+i] = object_data
                    outjson_list_0x1300_voltage.append(object_data)
            #--------------------------------------------------------------------------#
                if f"0x{(0x2000 + i):04X}" in jdata:
                    # 0x2000, throttle, int32_t rpm_speed; 回転速度
                    strdata = jdata[(f"0x{(0x2000 + i):04X}")].split()
                    data = (int(strdata[3], 16)<<24 | int(strdata[2], 16)<<16 | int(strdata[1], 16)<<8 | int(strdata[0], 16))
                    if data >= 0x80000000:
                        data -= 0x100000000  # 2の補数を利用して負の値に変換
                    object_data = {}
                    object_data["title"] = "Throttle No." + str(i)
                    #object_data["data"] = round(  (data/10.0) , 2)
                    object_data["data"] = data
                    object_data["raw"] = ("0x"+format(data, '08X'))
                    object_data["unit"] = " RPM"
                    #print(object_data)
                    #outjson.append(object_data)  
                    outjson[number_of_devices*1+i] = object_data
                    outjson_list_0x2000_throttle.append(object_data)
            #--------------------------------------------------------------------------#
                #elif f"0x{(0x2100 + i):04X}" in jdata:
                #    strdata = jdata[(f"0x{(0x2100 + i):04X}")].split()
                #    data = (int(strdata[0], 16)<<8 | int(strdata[1], 16))
                #    object_data = {}
                #    object_data["title"] = "Act throttle No." + str(i)
                #    object_data["data"] = data
                #    object_data["raw"] = ("0x"+format(data, '04X'))
                #    object_data["unit"] = " "
                #    print(object_data)
                #    #outjson.append(object_data)  
                #    outjson[number_of_devices*2+i] = object_data
            #--------------------------------------------------------------------------#
                if f"0x{(0x2200 + i):04X}" in jdata:
                    # 0x2200, current, int16_t bus_current; バス電流, 0.1A
                    strdata = jdata[(f"0x{(0x2200 + i):04X}")].split()
                    data = (int(strdata[1], 16)<<8 | int(strdata[0], 16))
                    if data >= 0x8000:
                        data -= 0x10000  # 2の補数を利用して負の値に変換
                    object_data = {}
                    object_data["title"] = "Bus current No." + str(i)
                    object_data["data"] = round( (data/10.0) , 1)
                    object_data["raw"] = ("0x"+format(data, '04X'))
                    object_data["unit"] = " A"
                    #print(object_data)
                    #outjson.append(object_data)  
                    outjson[number_of_devices*2+i] = object_data
                    outjson_list_0x2200_current.append(object_data)
            #--------------------------------------------------------------------------#
                #elif f"0x{(0x2300 + i):04X}" in jdata:
                #    strdata = jdata[(f"0x{(0x2300 + i):04X}")].split()
                #    data = (int(strdata[0], 16)<<8 | int(strdata[1], 16))
                #    object_data["title"] = "Phase current No." + str(i)
                #    object_data["data"] = data
                #    object_data["raw"] = ("0x"+format(data, '04X'))
                #    object_data["unit"] = " "
                #    print(object_data)
                    #outjson.append(object_data)  
                #    outjson[number_of_devices*4+i] = object_data
            #--------------------------------------------------------------------------#
                if i == 0x0F:
                    if f"0x{(0x2500 + 0x0F):04X}" in jdata:
                        #0x250F, voltage, uint16_t Low_voltage_battery_voltage; Lowバッテリー電圧, 0.1V
                        strdata = jdata[(f"0x{(0x2500 + 0x0F):04X}")].split()
                        data = (int(strdata[1], 16)<<8 | int(strdata[0], 16))
                        object_data = {}
                        object_data["title"] = "LV Battery Voltage"
                        object_data["data"] = round( (data/10.0) ,1)
                        temp_lv_bat_vol = round( (data/10.0) ,1)
                        object_data["raw"] = ("0x"+format(data, '04X'))
                        object_data["unit"] = " V"
                        #print(object_data)
                        #outjson.append(object_data)
                        outjson[number_of_devices*3+1] = object_data
                        outjson_list_0x2500_lv_voltage.append(object_data)
                    else:
                        #0x250F, voltage, uint16_t Low_voltage_battery_voltage; Lowバッテリー電圧, 0.1V, 信号が来てない場合
                        object_data = {}
                        object_data["title"] = "LV Battery Voltage"
                        object_data["data"] = temp_lv_bat_vol
                        object_data["raw"] = "0x0000"
                        object_data["unit"] = " V"
                        #print(object_data)
                        #outjson.append(object_data)
                        outjson[number_of_devices*3+1] = object_data
                        outjson_list_0x2500_lv_voltage.append(object_data)
                    
                    if f"0x{(0x6000 + 0x0F):04X}" in jdata:
                        # 0x600F, flight mode 切り替え, uint8_t 
                        strdata = jdata[(f"0x{(0x6000 + 0x0F):04X}")].split()
                        data = int(strdata[0], 16)
                        if data == 0x00:
                            # どんなCurrent_stateでもStandbyに遷移
                            Current_state = State.Standby
                            #Count_seconds_Supply_Relay_Precharge = 0
                            #Count_seconds_Motor_Relay_Precharge = 0
                        elif data == 0x01:
                            if Current_state == State.Standby:
                                Current_state = State.Supplying_Precharge
                            else:
                                # Current_stateがStandby以外の場合は遷移しない
                                None
                        elif data == 0x02:
                            None
                            #この状態には遷移しない
                            #Current_state = State.Supplying_Intermediate
                        elif data == 0x03:
                            None
                            #この状態には遷移しない
                            #Current_state = State.Supplying
                        elif data == 0x04:
                            if Current_state == State.Standby:
                                Current_state = State.Flying_Supply_Precharge
                            else:
                                # Current_stateがStandby以外の場合は遷移しない
                                None
                        elif data == 0x05:
                            None
                            #この状態には遷移しない
                            #Current_state = State.Flying_Supply_Intermediate
                        elif data == 0x06:
                            None
                            #この状態には遷移しない
                            #Current_state = State.Flying_Supply_only
                        elif data == 0x07:
                            None
                            #この状態には遷移しない
                            #Current_state = State.Flying_ESC_Precharge
                        elif data == 0x08:
                            None
                            #この状態には遷移しない
                            #Current_state = State.Flying_ESC_Intermediate
                        elif data == 0x09:
                            None
                            #この状態には遷移しない
                            #Current_state = State.Flying
                        elif data == 0x0A:
                            if Current_state == State.Standby:
                                Current_state = State.Discharge_Precharge
                            else:
                                # Current_stateがStandby以外の場合は遷移しない
                                None
                        elif data == 0x0B:
                            None
                            #この状態には遷移しない
                            #Current_state = State.Discharge_Intermediate
                        elif data == 0x0C:
                            None
                            #この状態には遷移しない
                            #Current_state = State.Discharge
                        elif data == 0x5A:
                            if Current_state == State.Standby:
                                Current_state = State.Manual
                            else:
                                # Current_stateがStandby以外の場合は遷移しない
                                None
                        else:
                            None
                            #この状態には遷移しない
                        #pass
                    #pass
                #pass                    
            except KeyError:
                pass
            #pass
        
        object_data = {}
        object_data["title"] = "STATE"
        object_data["data"] = Current_state.value
        object_data["raw"] = Current_state.name
        object_data["unit"] = Current_state.name
        object_data["State"] = Current_state.name
        outjson[number_of_devices*3+0] = object_data
        outjson_list_0x6000_mode.append(object_data)

        outjson_list.append(outjson_list_0x1300_voltage)
        outjson_list.append(outjson_list_0x2000_throttle)
        outjson_list.append(outjson_list_0x2200_current)
        outjson_list.append(outjson_list_0x6000_mode)
        outjson_list.append(outjson_list_0x2500_lv_voltage)

        with open('/mnt/ramdisk/outputv1.json', 'w') as f:
            if outjson != {}:
                json.dump(outjson, f)
            outjson_old = outjson
            #print(jdata)
            jdata = {}

        with open('/mnt/ramdisk/output.json', 'w') as f:
            if outjson_list != [[], [], [], [{'title': 'STATE', 'data': 0, 'raw': 'Standby', 'unit': 'Standby', 'State': 'Standby'}], [{'title': 'LV Battery Voltage', 'data': 0.0, 'raw': '0x0000', 'unit': ' V'}]]:
                json.dump(outjson_list, f)
                print(outjson_list)
            outjson_list_old = outjson_list
            outjson_list = []
            outjson_list_0x1300_voltage = []
            outjson_list_0x2000_throttle = []
            outjson_list_0x2200_current = []
            outjson_list_0x6000_mode = []
            outjson_list_0x2500_lv_voltage = []
        
        previous_time = current_time
        
        if Current_state == State.Standby:
            Count_seconds_Supply_Relay_Precharge = 0
            Count_seconds_Motor_Relay_Precharge = 0

            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x00], is_extended_id=True))  # 01 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x00], is_extended_id=True))  # 02 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x00], is_extended_id=True))  # 03 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x00], is_extended_id=True))  # 04 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x00], is_extended_id=True))  # 05 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x00], is_extended_id=True))  # 06 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x00], is_extended_id=True))  # 07 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x00], is_extended_id=True))  # 08 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x00], is_extended_id=True))  # 09 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x00], is_extended_id=True))  # 0A motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x00], is_extended_id=True))  # 0B motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x00], is_extended_id=True))  # 0C motor, OFF

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x00], is_extended_id=True))  # 21 500A Relay, OFF
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x00], is_extended_id=True))  # 22 500A Relay, OFF

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x00], is_extended_id=True))  # 0F patrol light, OFF
        elif Current_state == State.Supplying_Precharge:
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x00], is_extended_id=True))  # 01 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x00], is_extended_id=True))  # 02 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x00], is_extended_id=True))  # 03 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x00], is_extended_id=True))  # 04 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x00], is_extended_id=True))  # 05 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x00], is_extended_id=True))  # 06 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x00], is_extended_id=True))  # 07 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x00], is_extended_id=True))  # 08 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x00], is_extended_id=True))  # 09 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x00], is_extended_id=True))  # 0A motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x00], is_extended_id=True))  # 0B motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x00], is_extended_id=True))  # 0C motor, OFF

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x80], is_extended_id=True))  # 21 500A Relay, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x80], is_extended_id=True))  # 22 500A Relay, precharge on

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x80], is_extended_id=True))  # 0F patrol light, 8 ON
            
            if Count_seconds_Supply_Relay_Precharge >= Wait_seconds_Supply_Relay_Precharge:
                Current_state = State.Supplying_Intermediate
            else:
                None
            Count_seconds_Supply_Relay_Precharge = Count_seconds_Supply_Relay_Precharge + 1
        elif Current_state == State.Supplying_Intermediate:
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x00], is_extended_id=True))  # 01 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x00], is_extended_id=True))  # 02 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x00], is_extended_id=True))  # 03 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x00], is_extended_id=True))  # 04 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x00], is_extended_id=True))  # 05 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x00], is_extended_id=True))  # 06 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x00], is_extended_id=True))  # 07 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x00], is_extended_id=True))  # 08 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x00], is_extended_id=True))  # 09 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x00], is_extended_id=True))  # 0A motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x00], is_extended_id=True))  # 0B motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x00], is_extended_id=True))  # 0C motor, OFF

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0xC0], is_extended_id=True))  # 21 500A Relay, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0xC0], is_extended_id=True))  # 22 500A Relay, intermedate: precharge and main relay ON

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x80], is_extended_id=True))  # 0F patrol light, 8 ON
            Current_state = State.Supplying
        elif Current_state == State.Supplying:
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x00], is_extended_id=True))  # 01 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x00], is_extended_id=True))  # 02 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x00], is_extended_id=True))  # 03 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x00], is_extended_id=True))  # 04 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x00], is_extended_id=True))  # 05 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x00], is_extended_id=True))  # 06 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x00], is_extended_id=True))  # 07 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x00], is_extended_id=True))  # 08 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x00], is_extended_id=True))  # 09 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x00], is_extended_id=True))  # 0A motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x00], is_extended_id=True))  # 0B motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x00], is_extended_id=True))  # 0C motor, OFF

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x40], is_extended_id=True))  # 21 500A Relay, main relay ON, supplying now
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x40], is_extended_id=True))  # 22 500A Relay, main relay ON, supplying now

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x80], is_extended_id=True))  # 0F patrol light, 8 ON
        elif Current_state == State.Flying_Supply_Precharge:
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x00], is_extended_id=True))  # 01 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x00], is_extended_id=True))  # 02 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x00], is_extended_id=True))  # 03 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x00], is_extended_id=True))  # 04 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x00], is_extended_id=True))  # 05 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x00], is_extended_id=True))  # 06 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x00], is_extended_id=True))  # 07 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x00], is_extended_id=True))  # 08 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x00], is_extended_id=True))  # 09 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x00], is_extended_id=True))  # 0A motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x00], is_extended_id=True))  # 0B motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x00], is_extended_id=True))  # 0C motor, OFF

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x80], is_extended_id=True))  # 21 500A Relay, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x80], is_extended_id=True))  # 22 500A Relay, precharge on

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x80], is_extended_id=True))  # 0F patrol light, 8 ON
            if Count_seconds_Supply_Relay_Precharge >= Wait_seconds_Supply_Relay_Precharge:
                Current_state = State.Flying_Supply_Intermediate
            else:
                None
            Count_seconds_Supply_Relay_Precharge = Count_seconds_Supply_Relay_Precharge + 1
        elif Current_state == State.Flying_Supply_Intermediate:
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x00], is_extended_id=True))  # 01 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x00], is_extended_id=True))  # 02 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x00], is_extended_id=True))  # 03 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x00], is_extended_id=True))  # 04 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x00], is_extended_id=True))  # 05 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x00], is_extended_id=True))  # 06 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x00], is_extended_id=True))  # 07 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x00], is_extended_id=True))  # 08 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x00], is_extended_id=True))  # 09 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x00], is_extended_id=True))  # 0A motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x00], is_extended_id=True))  # 0B motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x00], is_extended_id=True))  # 0C motor, OFF

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0xC0], is_extended_id=True))  # 21 500A Relay, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0xC0], is_extended_id=True))  # 22 500A Relay, intermedate: precharge and main relay ON

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x80], is_extended_id=True))  # 0F patrol light, 8 ON
            Current_state = State.Flying_Supply_only
        elif Current_state == State.Flying_Supply_only:
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x00], is_extended_id=True))  # 01 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x00], is_extended_id=True))  # 02 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x00], is_extended_id=True))  # 03 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x00], is_extended_id=True))  # 04 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x00], is_extended_id=True))  # 05 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x00], is_extended_id=True))  # 06 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x00], is_extended_id=True))  # 07 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x00], is_extended_id=True))  # 08 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x00], is_extended_id=True))  # 09 motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x00], is_extended_id=True))  # 0A motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x00], is_extended_id=True))  # 0B motor, OFF
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x00], is_extended_id=True))  # 0C motor, OFF

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x40], is_extended_id=True))  # 21 500A Relay, main relay ON, supplying now
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x40], is_extended_id=True))  # 22 500A Relay, main relay ON, supplying now

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x80], is_extended_id=True))  # 0F patrol light, 8 ON
            Current_state = State.Flying_ESC_Precharge
        elif Current_state == State.Flying_ESC_Precharge:
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x80], is_extended_id=True))  # 01 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x80], is_extended_id=True))  # 02 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x80], is_extended_id=True))  # 03 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x80], is_extended_id=True))  # 04 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x80], is_extended_id=True))  # 05 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x80], is_extended_id=True))  # 06 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x80], is_extended_id=True))  # 07 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x80], is_extended_id=True))  # 08 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x80], is_extended_id=True))  # 09 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x80], is_extended_id=True))  # 0A motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x80], is_extended_id=True))  # 0B motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x80], is_extended_id=True))  # 0C motor, precharge on

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x40], is_extended_id=True))  # 21 500A Relay, main relay ON, supplying now
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x40], is_extended_id=True))  # 22 500A Relay, main relay ON, supplying now

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x80], is_extended_id=True))  # 0F patrol light, 8 ON
            if Count_seconds_Motor_Relay_Precharge >= Wait_seconds_Motor_Relay_Precharge:
                Current_state = State.Flying_ESC_Intermediate
            else:
                None
            Count_seconds_Motor_Relay_Precharge = Count_seconds_Motor_Relay_Precharge + 1
        elif Current_state == State.Flying_ESC_Intermediate:
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0xC0], is_extended_id=True))  # 01 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0xC0], is_extended_id=True))  # 02 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0xC0], is_extended_id=True))  # 03 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0xC0], is_extended_id=True))  # 04 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0xC0], is_extended_id=True))  # 05 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0xC0], is_extended_id=True))  # 06 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0xC0], is_extended_id=True))  # 07 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0xC0], is_extended_id=True))  # 08 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0xC0], is_extended_id=True))  # 09 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0xC0], is_extended_id=True))  # 0A motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0xC0], is_extended_id=True))  # 0B motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0xC0], is_extended_id=True))  # 0C motor, intermedate: precharge and main relay ON

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x40], is_extended_id=True))  # 21 500A Relay, main relay ON, supplying now
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x40], is_extended_id=True))  # 22 500A Relay, main relay ON, supplying now

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x80], is_extended_id=True))  # 0F patrol light, 8 ON
            Current_state = State.Flying
        elif Current_state == State.Flying:
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x40], is_extended_id=True))  # 01 motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x40], is_extended_id=True))  # 02 motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x40], is_extended_id=True))  # 03 motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x40], is_extended_id=True))  # 04 motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x40], is_extended_id=True))  # 05 motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x40], is_extended_id=True))  # 06 motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x40], is_extended_id=True))  # 07 motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x40], is_extended_id=True))  # 08 motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x40], is_extended_id=True))  # 09 motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x40], is_extended_id=True))  # 0A motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x40], is_extended_id=True))  # 0B motor, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x40], is_extended_id=True))  # 0C motor, main relay ON, ready to flying

            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x40], is_extended_id=True))  # 21 500A Relay, main relay ON, ready to flying
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x40], is_extended_id=True))  # 22 500A Relay, main relay ON, ready to flying

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0xC0], is_extended_id=True))  # 0F patrol light, 8 and 4 ON
        elif Current_state == State.Discharge_Precharge:
            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x00], is_extended_id=True))  # 21 500A Relay, main relay OFF
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x00], is_extended_id=True))  # 22 500A Relay, main relay OFF

            time.sleep(0.3)
            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x80], is_extended_id=True))  # 01 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x80], is_extended_id=True))  # 02 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x80], is_extended_id=True))  # 03 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x80], is_extended_id=True))  # 04 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x80], is_extended_id=True))  # 05 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x80], is_extended_id=True))  # 06 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x80], is_extended_id=True))  # 07 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x80], is_extended_id=True))  # 08 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x80], is_extended_id=True))  # 09 motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x80], is_extended_id=True))  # 0A motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x80], is_extended_id=True))  # 0B motor, precharge on
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x80], is_extended_id=True))  # 0C motor, precharge on

            if Count_seconds_Motor_Relay_Precharge >= Wait_seconds_Motor_Relay_Precharge:
                Current_state = State.Discharge_Intermediate
            else:
                None
            Count_seconds_Motor_Relay_Precharge = Count_seconds_Motor_Relay_Precharge + 1
        elif Current_state == State.Discharge_Intermediate:
            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x00], is_extended_id=True))  # 21 500A Relay, main relay OFF
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x00], is_extended_id=True))  # 22 500A Relay, main relay OFF

            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0xC0], is_extended_id=True))  # 01 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0xC0], is_extended_id=True))  # 02 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0xC0], is_extended_id=True))  # 03 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0xC0], is_extended_id=True))  # 04 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0xC0], is_extended_id=True))  # 05 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0xC0], is_extended_id=True))  # 06 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0xC0], is_extended_id=True))  # 07 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0xC0], is_extended_id=True))  # 08 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0xC0], is_extended_id=True))  # 09 motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0xC0], is_extended_id=True))  # 0A motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0xC0], is_extended_id=True))  # 0B motor, intermedate: precharge and main relay ON
            time.sleep(0.1)
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0xC0], is_extended_id=True))  # 0C motor, intermedate: precharge and main relay ON
            
            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x40], is_extended_id=True))  # 0F patrol light, 4 ON
            Current_state = State.Discharge
        elif Current_state == State.Discharge:
            can_bus.send(can.Message(arbitration_id=0x00001221, data=[0x00], is_extended_id=True))  # 21 500A Relay, main relay OFF
            can_bus.send(can.Message(arbitration_id=0x00001222, data=[0x00], is_extended_id=True))  # 22 500A Relay, main relay OFF

            can_bus.send(can.Message(arbitration_id=0x00001201, data=[0x40], is_extended_id=True))  # 01 motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x00001202, data=[0x40], is_extended_id=True))  # 02 motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x00001203, data=[0x40], is_extended_id=True))  # 03 motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x00001204, data=[0x40], is_extended_id=True))  # 04 motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x00001205, data=[0x40], is_extended_id=True))  # 05 motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x00001206, data=[0x40], is_extended_id=True))  # 06 motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x00001207, data=[0x40], is_extended_id=True))  # 07 motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x00001208, data=[0x40], is_extended_id=True))  # 08 motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x00001209, data=[0x40], is_extended_id=True))  # 09 motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x0000120A, data=[0x40], is_extended_id=True))  # 0A motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x0000120B, data=[0x40], is_extended_id=True))  # 0B motor, main relay ON, discharging from ESC
            can_bus.send(can.Message(arbitration_id=0x0000120C, data=[0x40], is_extended_id=True))  # 0C motor, main relay ON, discharging from ESC

            can_bus.send(can.Message(arbitration_id=0x0000120F, data=[0x40], is_extended_id=True))  # 0F patrol light, 4 ON
        elif Current_state == State.Manual:
            # なにもしない、手動でコマンドを入力する、機体の試験やメンテナンス用
            None
        else:
            # None, この状態には遷移しない
            can_bus.send(can.Message(arbitration_id=0x000012FF, data=[0x00], is_extended_id=True))  # FF all OFF
        #pass
    #time.sleep(0.001)
#print("")




