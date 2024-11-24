import can
import random
import time
from datetime import datetime, timedelta

can1 = can.interface.Bus(channel='can0', interface='socketcan')
previous_time = datetime.now()
CNT = 0
while True:
    current_time = datetime.now()  # 現在の時刻を取得
    if current_time.second != previous_time.second:
        jdata = {}
        for i in range(49):
            data = [random.randint(0,255) for _ in range(8)]
            msg = can.Message(
                arbitration_id=i, #random.randint(0,0x1FFFFFFF) ,
                data = data,
                is_extended_id=True)
            CNT = CNT +1
            can1.send(msg)
            print("0x" + format(msg.arbitration_id, '08X'))
            tmp = ""
            for i in range(msg.dlc):
                tmp = tmp + format(msg.data[i], '02X') + " "
            tmp = tmp[:-1]
            print(tmp)
            time.sleep(0.01)
        previous_time = current_time 

    #time.sleep(1)
