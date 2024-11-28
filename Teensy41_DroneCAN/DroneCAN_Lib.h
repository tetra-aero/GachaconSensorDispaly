#include <stdint.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

#include <Arduino.h>
#include <FlexCAN_T4.h>

void send_DroneCAN(CAN_message_t msg)
{
  can2.write(msg);
}

int8_t get_DroneCAN( CAN_message_t *msg)
{
    for(int i=0;i<10;i++)
    {
        if ( can2.read(*msg) ) {

            return 0;
        }
        delay(1);
    }
    return -1;
}

typedef struct {
    uint32_t    Source_Node_ID ;
    uint32_t    Target_Node_ID ;
    uint8_t    Service_Type ;
    uint8_t    Frame_Type ;
    uint8_t    Data_ID ;
    uint8_t    Priority ;
} IDField;
typedef struct {
    uint32_t    Transmission_ID;
    uint8_t    Toggle_bit;
    uint8_t    End_transfer ;
    uint8_t    Start_transfer ;
} Payload;



void getIDField(IDField *idfield,uint32_t can_raw_id)
{
    uint32_t FRAME_TYPE_MASK = 0x01<<7;         // ビット7
    uint8_t FRAME_TYPE = (can_raw_id & FRAME_TYPE_MASK) >> 7;
    idfield->Frame_Type = FRAME_TYPE;

    uint32_t PRIORITY_MASK;
    uint32_t DATA_MASK;
    uint32_t SOURCE_NODE_ID_MASK;
    uint32_t DATA_ID_MASK;
    uint32_t SERVICE_TYPE_MASK;
    uint32_t TARGET_NODE_ID_MASK;

    if(FRAME_TYPE==0)
    {
        PRIORITY_MASK = 0x1F << 24;        // ビット28-24
        DATA_MASK = 0xFFFF << 8;           //ビット23-8
        SOURCE_NODE_ID_MASK = 0x7F;        // ビット13-0        
    }
    if(FRAME_TYPE==1)
    {
            PRIORITY_MASK = 0x1F << 24;        //ビット28-24
            idfield->Priority =  (can_raw_id & PRIORITY_MASK)>>24;     
            DATA_ID_MASK = 0xFF << 16;           //ビット23-16
            idfield->Data_ID =  (can_raw_id & DATA_ID_MASK)>>16;          
            SERVICE_TYPE_MASK = 0x01<<15;        // ビット15
            idfield->Service_Type  =  (can_raw_id & SERVICE_TYPE_MASK)>>15;            
            TARGET_NODE_ID_MASK = 0x7F<<8;        //ビット14-8
            idfield->Target_Node_ID =  (can_raw_id & TARGET_NODE_ID_MASK)>>8;
            SOURCE_NODE_ID_MASK = 0x7F;           //ビット6-0
            idfield->Source_Node_ID =  (can_raw_id & SOURCE_NODE_ID_MASK); 
    }
        
}
uint32_t setIDField(IDField *idfield)
{


  return  idfield->Priority<<24 | idfield->Data_ID<<16 | (0x01<<15) | idfield->Target_Node_ID<<8 | (0x01<<7) | idfield->Source_Node_ID<<0;

    
}
void getDatafield(Payload *payload,uint8_t *can_raw_data,uint16_t can_dlc)
{
        uint32_t TRANSMISSON_ID_MASK = 0x1F;
        uint32_t TOGGLE_BIT_MASK = 0x01<<5;
        uint32_t END_TRANSFER_MASK = 0x01<<6;
        uint32_t STERT_TRANSFER_MASK = 0x01<<7;        
        payload->Transmission_ID =  (TRANSMISSON_ID_MASK & can_raw_data[can_dlc-1]);
        payload->Toggle_bit      =  (TOGGLE_BIT_MASK & can_raw_data[can_dlc-1])>>5;
        payload->End_transfer    =  (END_TRANSFER_MASK & can_raw_data[can_dlc-1])>>6;
        payload->Start_transfer  =  (STERT_TRANSFER_MASK & can_raw_data[can_dlc-1])>>7;
        //printf("getDatafield 0x%02X \n",can_raw_data[can_dlc-1]);
}

//===================================================================================//
// Set the digital throttle 2 
// Data ID 213
//===================================================================================//
#pragma pack(push, 1) //パディングを無効化
typedef struct {
    uint16_t CRC;               // CRCエラーなどの確認用
    uint16_t recv_pwm;               // 受信したPWM信号の値
    uint16_t comm_pwm;               // 通信で送信されるPWM信号の値
    int32_t speed;                // 回転速度
    int16_t current;              // モーターの電流
    int16_t bus_current;          // バス電流
    uint16_t voltage;              // 電圧
    uint16_t v_modulation;         // 電圧の変調率
    int16_t mos_temp;             // MOSFET温度
    int16_t cap_temp;             // コンデンサ温度
    int16_t mcu_temp;             // MCU温度
    uint16_t running_error;     // 実行時エラー
    uint16_t selfcheck_error;   // セルフチェックエラー
    int16_t motor_temp;           // モーター温度
    uint16_t time_10ms;         // 時間（10ミリ秒単位）
    uint8_t resv[3];              // 予約領域またはその他の情報
} MotorStatus;
#pragma pack(push, 0)


void DroneCAN_Debug(IDField *idfield,Payload *payload)
{
            printf("Source_Node_ID: %u\n", idfield->Source_Node_ID);
            printf("Target_Node_ID: %u\n", idfield->Target_Node_ID);
            printf("Service_Type: %u\n", idfield->Service_Type);
            printf("Frame_Type: %u\n", idfield->Frame_Type);
            printf("Data_ID: %u\n", idfield->Data_ID);
            printf("Priority: %u\n", idfield->Priority);
            
            printf("Transmission_ID: %u\n", payload->Transmission_ID);
            printf("Start_transfer: %u\n", payload->Start_transfer);
            printf("Toggle_bit: %u\n", payload->Toggle_bit);
            printf("End_transfer: %u\n", payload->End_transfer);

}


uint8_t DroneCAN_DataID_213(uint16_t pwm,MotorStatus *mstatus)
{
    
        
        IDField idfield;
        Payload payload;
        uint8_t multi_frame_flag = 0;
        uint8_t multi_frame_buf[32*8];
        uint8_t multi_frame_length = 0;

        char S1[200];
        idfield.Source_Node_ID = 64;
        idfield.Target_Node_ID = 32;
        idfield.Service_Type = 1;
        idfield.Frame_Type = 1;
        idfield.Data_ID = 213;
        idfield.Priority = 0;
        uint32_t id = setIDField(&idfield);
        CAN_message_t can_message;
        can_message.id =  setIDField(&idfield);
        can_message.flags.extended = true;
        can_message.len = 3;
        can_message.buf[0] = 0xFF & pwm;
        can_message.buf[1] = pwm>>8;
        can_message.buf[2] = 0xC0;
        send_DroneCAN(can_message);
        //
        //printf("CANID : 0x%08X \n");
        for(int i=0;i<10;i++)
        //while(1)
        {        
         
          if(get_DroneCAN(&can_message)==0)
          {
          
            uint32_t can_raw_id = can_message.id;
            getIDField(&idfield,can_message.id);
            getDatafield(&payload,can_message.buf,can_message.len);

            /*
            Serial.print("get_DroneCAN can2 "); 
            Serial.print("  ID: 0x"); Serial.print(can_message.id, HEX );
            Serial.print("  LEN: "); Serial.print(can_message.len);
            Serial.print(" DATA: ");
            for ( uint8_t i = 0; i < can_message.len; i++ ) {
                Serial.print(can_message.buf[i],HEX); Serial.print(" ");
            }
            Serial.println();
          
            printf("Source_Node_ID: %u\n", idfield.Source_Node_ID);
            printf("Target_Node_ID: %u\n", idfield.Target_Node_ID);
            printf("Service_Type: %u\n", idfield.Service_Type);
            printf("Frame_Type: %u\n", idfield.Frame_Type);
            printf("Data_ID: %u\n", idfield.Data_ID);
            printf("Priority: %u\n", idfield.Priority);
            
            printf("Transmission_ID: %u\n", payload.Transmission_ID);
            printf("Start_transfer: %u\n", payload.Start_transfer);
            printf("Toggle_bit: %u\n", payload.Toggle_bit);
            printf("End_transfer: %u\n", payload.End_transfer);
  */
          

            if( payload.Start_transfer ==1 && payload.End_transfer ==1)
            {
                    multi_frame_flag =0;
            }
            if( payload.Start_transfer ==1 && payload.End_transfer ==0  )
            { 
                multi_frame_flag = 1;
                multi_frame_length = 0;
                for(int i=0;i<(can_message.len-1);i++)
                    multi_frame_buf[multi_frame_length+i] = can_message.buf[i];
                multi_frame_length = multi_frame_length + can_message.len-1;
            }
            if(payload.Start_transfer==0  && payload.End_transfer==0 && multi_frame_flag==1)
            {
                for(int i=0;i<(can_message.len-1);i++)
                    multi_frame_buf[multi_frame_length+i] = can_message.buf[i];
                multi_frame_length = multi_frame_length + can_message.len-1;
            }
            if(payload.Start_transfer==0 && payload.End_transfer==1  && multi_frame_flag==1)
            {
                for(int i=0;i<(can_message.len-1);i++)
                    multi_frame_buf[multi_frame_length+i] = can_message.buf[i];
                multi_frame_length = multi_frame_length + can_message.len-1;

                multi_frame_flag = 0;
                printf("multi_frame_length:%d \r\n",multi_frame_length);
                if( idfield.Data_ID==213 && multi_frame_length==35)
                {
                    memcpy(mstatus, multi_frame_buf, multi_frame_length);
                    return 0;
                }
            }
          }
        }
}

uint8_t DroneCAN_DataID_211(MotorStatus *mstatus)
{
    
        
        IDField idfield;
        Payload payload;
        uint8_t multi_frame_flag = 0;
        uint8_t multi_frame_buf[32*8];
        uint8_t multi_frame_length = 0;

        char S1[200];
        idfield.Source_Node_ID = 64;
        idfield.Target_Node_ID = 32;
        idfield.Service_Type = 1;
        idfield.Frame_Type = 1;
        idfield.Data_ID = 211;
        idfield.Priority = 0;
        uint32_t id = setIDField(&idfield);
        CAN_message_t can_message;
        can_message.id =  setIDField(&idfield);
        can_message.flags.extended = true;
        can_message.len = 1;
        can_message.buf[0] = 0xC0;
        send_DroneCAN(can_message);
        //
        //printf("CANID : 0x%08X \n");
        for(int i=0;i<1000;i++)
        //while(1)
        {        
         
          if(get_DroneCAN(&can_message)==0)
          {
          
            uint32_t can_raw_id = can_message.id;
            getIDField(&idfield,can_message.id);
            getDatafield(&payload,can_message.buf,can_message.len);

            /*
            Serial.print("get_DroneCAN can2 "); 
            Serial.print("  ID: 0x"); Serial.print(can_message.id, HEX );
            Serial.print("  LEN: "); Serial.print(can_message.len);
            Serial.print(" DATA: ");
            for ( uint8_t i = 0; i < can_message.len; i++ ) {
                Serial.print(can_message.buf[i],HEX); Serial.print(" ");
            }
            Serial.println();
          
            printf("Source_Node_ID: %u\n", idfield.Source_Node_ID);
            printf("Target_Node_ID: %u\n", idfield.Target_Node_ID);
            printf("Service_Type: %u\n", idfield.Service_Type);
            printf("Frame_Type: %u\n", idfield.Frame_Type);
            printf("Data_ID: %u\n", idfield.Data_ID);
            printf("Priority: %u\n", idfield.Priority);
            
            printf("Transmission_ID: %u\n", payload.Transmission_ID);
            printf("Start_transfer: %u\n", payload.Start_transfer);
            printf("Toggle_bit: %u\n", payload.Toggle_bit);
            printf("End_transfer: %u\n", payload.End_transfer);
            */
          

            if( payload.Start_transfer ==1 && payload.End_transfer ==1)
            {
                    multi_frame_flag =0;
            }
            if( payload.Start_transfer ==1 && payload.End_transfer ==0  )
            { 
                multi_frame_flag = 1;
                multi_frame_length = 0;
                for(int i=0;i<(can_message.len-1);i++)
                    multi_frame_buf[multi_frame_length+i] = can_message.buf[i];
                multi_frame_length = multi_frame_length + can_message.len-1;
            }
            if(payload.Start_transfer==0  && payload.End_transfer==0 && multi_frame_flag==1)
            {
                for(int i=0;i<(can_message.len-1);i++)
                    multi_frame_buf[multi_frame_length+i] = can_message.buf[i];
                multi_frame_length = multi_frame_length + can_message.len-1;
            }
            if(payload.Start_transfer==0 && payload.End_transfer==1  && multi_frame_flag==1)
            {
                for(int i=0;i<(can_message.len-1);i++)
                    multi_frame_buf[multi_frame_length+i] = can_message.buf[i];
                multi_frame_length = multi_frame_length + can_message.len-1;

                multi_frame_flag = 0;
                printf("multi_frame_length:%d \r\n",multi_frame_length);
                if( idfield.Data_ID==211 && multi_frame_length==35)
                {
                    memcpy(mstatus, multi_frame_buf, multi_frame_length);
                    return 0;
                }
            }
          }
        }
        return 1;
}
