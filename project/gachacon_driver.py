import json
from pathlib import Path
import datetime
import time
import requests
import can
from datetime import datetime, timedelta
jdata = {}
CNT = 0

with open('config.json', 'r') as f:
    config = json.load(f)

can = can.interface.Bus(channel=config['can_json']['can_channel'], interface='socketcan')
previous_time = datetime.now()


outjson = [0 for _ in range(14*3)]
outjson_old = [0 for _ in range(14*3)]

while 1:
    current_time = datetime.now()  # 現在の時刻を取得
    msg = can.recv(2.0)
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
        for i in range(0x0E):
            try:
            #--------------------------------------------------------------------------#
                if f"0x{(0x1300 + i):04X}" in jdata:
                    strdata = jdata[(f"0x{(0x1300 + i):04X}")].split()
                    data = (int(strdata[0], 16)<<8 | int(strdata[1], 16))
                    object_data = {}
                    object_data["title"] = "Battery Voltage No." + str(i+1)
                    object_data["data"] = round( (data/10) ,0)
                    object_data["raw"] = ("0x"+format(data, '04X'))
                    object_data["unit"] = " V"
                    print(object_data)
                    #outjson.append(object_data)
                    outjson[14*0+i] = object_data
            #--------------------------------------------------------------------------#
                if f"0x{(0x2000 + i):04X}" in jdata:
                    strdata = jdata[(f"0x{(0x2000 + i):04X}")].split()
                    data = (int(strdata[0], 16)<<8 | int(strdata[1], 16))
                    object_data = {}
                    object_data["title"] = "Throttle No." + str(i+1)
                    object_data["data"] = round( ((data/1024.0)*100.0) , 2)
                    object_data["raw"] = ("0x"+format(data, '04X'))
                    object_data["unit"] = " RPM"
                    print(object_data)
                    #outjson.append(object_data)  
                    outjson[14*1+i] = object_data
            #--------------------------------------------------------------------------#
                #elif f"0x{(0x2100 + i):04X}" in jdata:
                #    strdata = jdata[(f"0x{(0x2100 + i):04X}")].split()
                #    data = (int(strdata[0], 16)<<8 | int(strdata[1], 16))
                #    object_data = {}
                #    object_data["title"] = "Act throttle No." + str(i+1)
                #    object_data["data"] = data
                #    object_data["raw"] = ("0x"+format(data, '04X'))
                #    object_data["unit"] = " "
                #    print(object_data)
                #    #outjson.append(object_data)  
                #    outjson[14*2+i] = object_data
            #--------------------------------------------------------------------------#
                if f"0x{(0x2200 + i):04X}" in jdata:
                    strdata = jdata[(f"0x{(0x2200 + i):04X}")].split()
                    data = (int(strdata[0], 16)<<8 | int(strdata[1], 16))
                    object_data = {}
                    object_data["title"] = "Bus current No." + str(i+1)
                    object_data["data"] = round( (data/64) , 2)
                    object_data["raw"] = ("0x"+format(data, '04X'))
                    object_data["unit"] = " A"
                    print(object_data)
                    #outjson.append(object_data)  
                    outjson[14*2+i] = object_data
            #--------------------------------------------------------------------------#
                #elif f"0x{(0x2300 + i):04X}" in jdata:
                #    strdata = jdata[(f"0x{(0x2300 + i):04X}")].split()
                #    data = (int(strdata[0], 16)<<8 | int(strdata[1], 16))
                #    object_data["title"] = "Phase current No." + str(i+1)
                #    object_data["data"] = data
                #    object_data["raw"] = ("0x"+format(data, '04X'))
                #    object_data["unit"] = " "
                #    print(object_data)
                    #outjson.append(object_data)  
                #    outjson[14*4+i] = object_data
            #--------------------------------------------------------------------------#
            except KeyError:
                pass
            
        with open('/mnt/ramdisk/output.json', 'w') as f:
            json.dump(outjson, f)
            outjson_old = outjson
            #print(jdata)
            jdata = {}
            previous_time = current_time
    #time.sleep(0.001)
print("")

