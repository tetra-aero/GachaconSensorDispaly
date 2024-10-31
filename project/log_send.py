import can
import random
import time
from datetime import datetime, timedelta
import re
can1 = can.interface.Bus(channel='can1', interface='socketcan')

# 正規表現を使ってタイムスタンプ、インターフェース、CAN ID、データフィールドに分解
#path = "../ESC_CAN_Log/candump-2024-10-11_160637.log"
#pattern = r"\((.*?)\)\s(\w+)\s(\w+)#(\w+)"
path = "../GACHACON_log/candump-2022-02-22_161128_test03-04.log"
pattern = r"\((\d+\.\d+)\)\s+(\S+)\s+([0-9A-F]+)#([0-9A-F]*)"

CNT = 0
while 1:
    with open(path) as f:
        for line in f:
            # 各行を処理
            input_str = line.strip()  # .strip() は行末の改行を削除するため
            print(input_str)        

            # マッチを確認
            match = re.match(pattern, input_str)
            
            if match:
                # 各要素にアクセス
                timestamp = match.group(1)
                interface = match.group(2)
                can_id = match.group(3)
                data = match.group(4)
                print("CAN ID: %s : %s" % (can_id,data))
                ID = int(can_id, 16)
                data =  [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
                msg = can.Message(
                    arbitration_id=ID, #random.randint(0,0x1FFFFFFF) ,
                    data = data,
                    is_extended_id=True)
                can1.send(msg)
                time.sleep(0.001)
            #if(CNT==5):
            #    break
            CNT = CNT+1
can1.shutdown()
print("End...")
exit()

