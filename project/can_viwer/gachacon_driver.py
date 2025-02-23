import json
from pathlib import Path
import datetime
import time
import requests
import can
from datetime import datetime, timedelta
from enum import Enum

class State(Enum):
    Stanby                      = 0
    Supplying_Precharge         = 1
    Supplying_Intermediate      = 2
    Supplying                   = 3
    Flying_Supply_Precharge     = 4
    Flying_Supply_Intermediate  = 5
    Flying_Supply_only          = 6
    Flying_ESC_Precharge        = 7
    Flying_ESC_Intermediate     = 8
    Flying                      = 9
    

Current_state = State.Stanby
jdata = {}

#can_bus = can.interface.Bus(channel="can0", interface='socketcan')
can_bus = can.interface.Bus(channel="vcan0", interface='socketcan')
previous_time = datetime.now()

number_of_devices = 0x23
number_of_element = number_of_devices*4

outjson = [0 for _ in range(number_of_element)]
outjson_old = [0 for _ in range(number_of_element)]

Wait_seconds_Supply_Relay_Precharge = 7
Count_seconds_Supply_Relay_Precharge = 0

Wait_seconds_Motor_Relay_Precharge = 7
Count_seconds_Motor_Relay_Precharge = 0


while 1:
    current_time = datetime.now()  # 現在の時刻を取得
    msg = can_bus.recv(2.0)
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

    #=========================================================================#
    ## 1秒起きに実行
    #=========================================================================#
    if current_time.second != previous_time.second:
        #print(jdata)
        for i in range(number_of_devices):
            try:
            #--------------------------------------------------------------------------#
                if f"0x{(0x1300 + i):04X}" in jdata:
                    strdata = jdata[(f"0x{(0x1300 + i):04X}")].split()
                    data = (int(strdata[1], 16)<<8 | int(strdata[0], 16))
                    object_data = {}
                    object_data["title"] = "Battery Voltage No." + str(i)
                    object_data["data"] = round( (data/10.0) ,2)
                    object_data["raw"] = ("0x"+format(data, '04X'))
                    object_data["unit"] = " V"
                    print(object_data)
                    #outjson.append(object_data)
                    outjson[number_of_devices*0+i] = object_data
            #--------------------------------------------------------------------------#
                if f"0x{(0x2000 + i):04X}" in jdata:
                    strdata = jdata[(f"0x{(0x2000 + i):04X}")].split()
                    data = (int(strdata[1], 16)<<8 | int(strdata[0], 16))
                    object_data = {}
                    object_data["title"] = "Throttle No." + str(i)
                    object_data["data"] = round(  (data/10.0) , 2)
                    object_data["raw"] = ("0x"+format(data, '04X'))
                    object_data["unit"] = " RPM"
                    print(object_data)
                    #outjson.append(object_data)  
                    outjson[number_of_devices*1+i] = object_data
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
                    strdata = jdata[(f"0x{(0x2200 + i):04X}")].split()
                    data = (int(strdata[1], 16)<<8 | int(strdata[0], 16))
                    if data >= 0x8000:
                        data -= 0x10000  # 2の補数を利用して負の値に変換
                    object_data = {}
                    object_data["title"] = "Bus current No." + str(i)
                    object_data["data"] = round( (data/10.0) , 1)
                    object_data["raw"] = ("0x"+format(data, '04X'))
                    object_data["unit"] = " A"
                    print(object_data)
                    #outjson.append(object_data)  
                    outjson[number_of_devices*2+i] = object_data
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
                if f"0x{(0x6000 + 0x0F):04X}" in jdata:
                    strdata = jdata[(f"0x{(0x6000 + 0x0F):04X}")].split()
                    data = int(strdata[0], 16)
                    if data == 0x00:
                        # どんなCurrent_stateでもStanbyに遷移
                        Current_state = State.Stanby
                        Count_seconds_Supply_Relay_Precharge = 0
                        Count_seconds_Motor_Relay_Precharge = 0
                    elif data == 0x01:
                        if Current_state == State.Stanby:
                            Current_state = State.Supplying_Precharge
                        else:
                            # Current_stateがStanby以外の場合は遷移しない
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
                        if Current_state == State.Stanby:
                            Current_state = State.Flying_Supply_Precharge
                        else:
                            # Current_stateがStanby以外の場合は遷移しない
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
                    else:
                        None
                        #この状態には遷移しない
                    #pass
                #pass                    
            except KeyError:
                pass
            #pass
        
        object_data = {}
        object_data["State"] = Current_state.name
        outjson[number_of_devices*3+0] = object_data

        with open('/mnt/ramdisk/output.json', 'w') as f:
            json.dump(outjson, f)
            outjson_old = outjson
            #print(jdata)
            jdata = {}
            previous_time = current_time
        
        if Current_state == State.Stanby:
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
        else:
            # None, この状態には遷移しない
            can_bus.send(can.Message(arbitration_id=0x000012FF, data=[0x00], is_extended_id=True))  # FF all OFF
        #pass
    #time.sleep(0.001)
print("")




