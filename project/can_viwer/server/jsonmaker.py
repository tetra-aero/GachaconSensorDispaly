import json
from pathlib import Path
import datetime
import time
import requests
from datetime import datetime, timedelta

url = 'http://localhost:1001/'


previous_time = datetime.now()
while(1):
    current_time = datetime.now()  # 現在の時刻を取得
    CNT=0
    if current_time.second != previous_time.second:
        r = requests.get(url)
        jdata = {}
        jdata = r.json()
        jdata_values = list(jdata.keys())
        jdata_items = list(jdata.values())
        #print(jdata)
        previous_time = current_time
        outjson = []
        for i in range(len(jdata)):
            object_data = {}
            object_data["title"] = "No." + jdata_values[i]
            object_data["data"] = jdata_items[i].split()[0]
            object_data["unit"] = "v"
            print(object_data)
            outjson.append(object_data)  
        with open('/mnt/ramdisk/output.json', 'w') as f:
            json.dump(outjson, f)
        previous_time = current_time
    time.sleep(0.1)
    #exit()