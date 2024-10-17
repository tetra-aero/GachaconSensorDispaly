import json
import time
import can
from datetime import datetime, timedelta

jdata = {}
CNT = 0

with open('config.json', 'r') as f:
    config = json.load(f)

can = can.interface.Bus(channel=config['can_json']['can_channel'], interface='socketcan')
previous_time = datetime.now()
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
    jdata["0x" +format(msg.arbitration_id, '08X')] = tmp
    CNT = CNT+1

    #with open('/mnt/ramdisk/test.json', 'r') as f:
    #    jdata = json.load(f)
    if current_time.second != previous_time.second:
        with open(config['can_json']['json'], 'w') as f:
            json.dump(jdata, f, indent=2)
        print(jdata)
        jdata = {}
        previous_time = current_time
    #time.sleep(0.001)
print("")