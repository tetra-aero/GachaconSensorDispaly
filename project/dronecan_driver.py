
import json
import time
import can
import struct
from datetime import datetime, timedelta

class DroneCAN:
    def __init__(self):
        self.ID  = {}
        self.ID["Source_Node_ID"] = 0
        self.ID["Target_Node_ID"] = 0
        self.ID["Service_Type"] = 0
        self.ID["Frame_Type"] = 0
        self.ID["Data_ID"] = 0
        self.ID["Priority"] = 0

        self.Payload = {}
        self.Payload["Transmission_ID"] = 0
        self.Payload["Toggle_bit"] = 0
        self.Payload["End_transfer"] = 0
        self.Payload["Start_transfer"] = 0
        
    def IDField(self,can_raw_id) :
        FRAME_TYPE_MASK = 0x01<<7         # ビット7
        FRAME_TYPE = (can_raw_id & FRAME_TYPE_MASK) >> 7
        self.ID["Frame_Type"] = FRAME_TYPE        
        if(FRAME_TYPE==0):
            print("Anonymous broadcast message frame ID")
            PRIORITY_MASK = 0x1F << 24        # ビット28-24
            DATA_MASK = 0xFFFF << 8           # ビット23-8
            SOURCE_NODE_ID_MASK = 0x7F               # ビット13-0
        if(FRAME_TYPE==1):
            #print("Service frame ID")
            PRIORITY_MASK = 0x1F << 24        # ビット28-24
            self.ID["Priority"] =  (can_raw_id & PRIORITY_MASK)>>24     
            DATA_ID_MASK = 0xFF << 16           # ビット23-16
            self.ID["Data_ID"] =  (can_raw_id & DATA_ID_MASK)>>16          
            SERVICE_TYPE_MASK = 0x01<<15               # ビット15
            self.ID["Service_Type"]  =  (can_raw_id & SERVICE_TYPE_MASK)>>15            
            TARGET_NODE_ID_MASK = 0x7F<<8               # ビット14-8
            self.ID["Target_Node_ID"] =  (can_raw_id & TARGET_NODE_ID_MASK)>>8
            SOURCE_NODE_ID_MASK = 0x7F               # ビット6-0
            self.ID["Source_Node_ID"] =  (can_raw_id & SOURCE_NODE_ID_MASK) 
    def Datafield(self,can_raw_data,can_dlc):
        #print(can_raw_data)
        TRANSMISSON_ID_MASK = 0x1F
        TOGGLE_BIT_MASK = 0x01<<5
        END_TRANSFER_MASK = 0x01<<6
        STERT_TRANSFER_MASK = 0x01<<7        
        self.Payload["Transmission_ID"] =  (TRANSMISSON_ID_MASK & can_raw_data[can_dlc-1])
        self.Payload["Toggle_bit"]      =  (TOGGLE_BIT_MASK & can_raw_data[can_dlc-1])>>5
        self.Payload["End_transfer"]    =  (END_TRANSFER_MASK & can_raw_data[can_dlc-1])>>6
        self.Payload["Start_transfer"]  =  (STERT_TRANSFER_MASK & can_raw_data[can_dlc-1])>>7


can0 = can.interface.Bus(channel='can0', interface='socketcan')
jdata = {}


multi_frame_flag = 0
multi_frame_buf = []
multi_frame_length = 0

while 1:
    msg = can0.recv(2.0)
    tmp = ""
    if msg:
        #print("-"*30)
        #print (msg)
        #print(msg.channel)
        #print(format(msg.arbitration_id, '02X'))
        dcan = DroneCAN()
        dcan.IDField(msg.arbitration_id)
        dcan.Datafield(msg.data,msg.dlc)
        #print("Data_ID:%d" % dcan.ID["Data_ID"])  
        tmp = ""

        #print("Transmission_ID:%d" % dcan.Payload["Transmission_ID"])  
        #print("Toggle_bit:%d" % dcan.Payload["Toggle_bit"])  
        #print("End_transfer:%d" % dcan.Payload["End_transfer"])  
        #print("Start_transfer:%d" % dcan.Payload["Start_transfer"])  
        if(dcan.Payload["End_transfer"]==1 and dcan.Payload["Start_transfer"]==1 ):
            multi_frame_flag =0
            pass
        if(dcan.Payload["End_transfer"]==0 and dcan.Payload["Start_transfer"]==1 ):
            multi_frame_flag = 1
            for i in range(msg.dlc-1):
                multi_frame_buf.append(msg.data[i])
            multi_frame_length = (multi_frame_length + msg.dlc-1)
        if(dcan.Payload["End_transfer"]==0 and dcan.Payload["Start_transfer"]==0 and multi_frame_flag==1):
            for i in range(msg.dlc-1):
                multi_frame_buf.append(msg.data[i])
            multi_frame_length = (multi_frame_length + msg.dlc-1)
        if(dcan.Payload["End_transfer"]==1 and dcan.Payload["Start_transfer"]==0 and multi_frame_flag==1):
            multi_frame_flag = 0
            for i in range(msg.dlc-1):
                multi_frame_buf.append(msg.data[i])
            multi_frame_length = (multi_frame_length + msg.dlc-1)
            #print("len:%d" % len(multi_frame_buf))
            if(dcan.ID["Data_ID"]==213 and multi_frame_length==35):
                fmt = "= H H H i h h H H h h h H H h H 3p"
                unpacked_data = struct.unpack(fmt,bytes(multi_frame_buf))
                namestr = [
                    "CRC",
                    "recv_pwm",
                    "comm_pwm",
                    "speed",
                    "current",
                    "bus_current",
                    "voltage",
                    "v_modulation",
                    "mos_temp",
                    "cap_temp",
                    "mcu_temp",
                    "running_error",
                    "selfcheck_error",
                    "motor_temp",
                    "time_10ms",
                    "resv"
                ]
                """
                for index, value in enumerate(unpacked_data):
                    if isinstance(value, bytes):  # 文字列 (bytes) の場合はデコードして表示
                        value = value.decode('utf-8').rstrip('\x00')  # NULL終端文字を除去
                    print(f"{namestr[index]} {index + 1}:     {value}")
                """
                if(unpacked_data[3]>=0):
                    print("-"*30)
                    print(f"{namestr[1]}:     {unpacked_data[1]}")
                    print(f"{namestr[2]}:     {unpacked_data[2]}")
                    print(f"{namestr[3]}:     {unpacked_data[3]}")
                    print(f"{namestr[4]}:     {unpacked_data[4]}")
                    print(f"{namestr[5]}:     {unpacked_data[5]}")
                    print(f"{namestr[6]}:     {unpacked_data[6]}")
                
                multi_frame_buf = []
                multi_frame_length = 0
            else:
                print("error")
                multi_frame_buf = []
                multi_frame_length = 0

    #jdata["0x" +format(msg.arbitration_id, '08X')] = tmp
