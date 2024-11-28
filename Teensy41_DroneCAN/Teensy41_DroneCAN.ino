// demo: CAN-BUS Shield, send data
#include <SPI.h>
#include <FlexCAN_T4.h>



FlexCAN_T4<CAN1, RX_SIZE_256, TX_SIZE_16> can1;
FlexCAN_T4<CAN2, RX_SIZE_256, TX_SIZE_16> can2;

#include "DroneCAN_Lib.h"

#define PIN_BIT0 6
#define PIN_BIT1 7
#define PIN_BIT2 8
#define PIN_BIT3 9
#define PIN_BIT4 32
#define PIN_BIT5 33
#define PIN_BIT6 40
#define PIN_BIT7 41


CAN_message_t msg;
uint32_t Gachacon_ID=0;
void setup() {
    SERIAL_PORT_MONITOR.begin(115200);
    //while( !Serial ) ;
  delay(1000);
  can2.begin();
  can2.setBaudRate(500000);
  can2.setMaxMB(16);
  can2.enableFIFO();
  //can2.enableFIFOInterrupt();
  //can2.onReceive(CANRecive);
  can2.mailboxStatus();

  can1.begin();
  can1.setBaudRate(125000);
  can1.setMaxMB(16);
  can1.enableFIFO();
  //can1.enableFIFOInterrupt();
  //can1.onReceive(CANRecive);
  can1.mailboxStatus();


    pinMode(PIN_BIT0, INPUT);
    pinMode(PIN_BIT1, INPUT);
    pinMode(PIN_BIT2, INPUT);
    pinMode(PIN_BIT3, INPUT);
    pinMode(PIN_BIT4, INPUT);
    pinMode(PIN_BIT5, INPUT);
    pinMode(PIN_BIT6, INPUT);
    pinMode(PIN_BIT7, INPUT);
    uint8_t hardcoder_val = (0x01 & (digitalRead(PIN_BIT0) << 0)) |
                            (0x02 & (digitalRead(PIN_BIT1) << 1)) |
                            (0x04 & (digitalRead(PIN_BIT2) << 2)) |
                            (0x08 & (digitalRead(PIN_BIT3) << 3)) |
                            (0x10 & (digitalRead(PIN_BIT4) << 4)) |
                            (0x20 & (digitalRead(PIN_BIT5) << 5)) |
                            (0x40 & (digitalRead(PIN_BIT6) << 6)) |
                            (0x80 & (digitalRead(PIN_BIT7) << 7));

  Gachacon_ID =  hardcoder_val & 0x3F;
    printf("Gachacon_ID Value: 0x%x\n", Gachacon_ID);
 Serial.println(" HELLO");
          msg.id = 0x0000 + Gachacon_ID;
          msg.flags.extended = 1;
          msg.len = 3;
          msg.buf[0] = 0x12;
          msg.buf[1] = 0x34;
          msg.buf[2] = 0x56;
          can1.write(msg);


}

unsigned char stmp[8] = {0, 1, 2, 3, 4, 5, 6, 7};

void CANRecive(const CAN_message_t &msg) {
    Serial.print("can2 "); 
    Serial.print("  ID: 0x"); Serial.print(msg.id, HEX );
    Serial.print("  LEN: "); Serial.print(msg.len);
    Serial.print(" DATA: ");
    for ( uint8_t i = 0; i < msg.len; i++ ) {
      Serial.print(msg.buf[i],HEX); Serial.print(" ");
    }
     Serial.println();
}


void loop() {
  //Serial.println(" CAN SEND");

        MotorStatus mstatus;
        //DroneCAN_DataID_213(8000,&mstatus);
        if(DroneCAN_DataID_211(&mstatus)==0)
        {
          printf("---------------------------------------------------\n");
          printf("CRC: %u\n", mstatus.CRC);
          printf("recv_pwm: %u\n", mstatus.recv_pwm);
          printf("comm_pwm: %u\n", mstatus.comm_pwm);
          printf("speed: %d\n", mstatus.speed);
          printf("current: %d\n", mstatus.current);
          printf("bus_current: %d\n", mstatus.bus_current);
          printf("voltage: %u\n", mstatus.voltage);
          printf("v_modulation: %u\n", mstatus.v_modulation);
          printf("mos_temp: %d\n", mstatus.mos_temp);
          printf("cap_temp: %d\n", mstatus.cap_temp);
          printf("mcu_temp: %d\n", mstatus.mcu_temp);
          printf("running_error: %u\n", mstatus.running_error);
          printf("selfcheck_error: %u\n", mstatus.selfcheck_error);
          printf("motor_temp: %d\n", mstatus.motor_temp);
          printf("time_10ms: %u\n", mstatus.time_10ms);
          printf("resv: %02X %02X %02X\n", mstatus.resv[0], mstatus.resv[1], mstatus.resv[2]);

          CAN_message_t msg;
          printf("Gachacon_ID Value: 0x%x\n", Gachacon_ID);
          msg.id = 0x1300 + Gachacon_ID;
          msg.flags.extended = 1;
          msg.len = 2;
          msg.buf[0] = 0xff & mstatus.voltage;
          msg.buf[1] = mstatus.voltage>>8;
          can1.write(msg);

          msg.id = 0x2000 + Gachacon_ID;
          msg.flags.extended = 1;
          msg.len = 2;
          msg.buf[0] = 0xff & mstatus.speed;
          msg.buf[1] = mstatus.speed>>8;
          can1.write(msg);

          msg.id = 0x2200 + Gachacon_ID;
          msg.flags.extended = 1;
          msg.len = 2;
          msg.buf[0] = 0xff & mstatus.bus_current;
          msg.buf[1] = mstatus.bus_current>>8;
          can1.write(msg);
          delay(1000);
        }
        else
        {
          printf("==== CAN Error ====\r\n");
        }

/*
for(int i=0;i<1000;i++)
{
  if ( can2.read(msg) ) {
        Serial.print("can2 "); 
      Serial.print("  ID: 0x"); Serial.print(msg.id, HEX );
      Serial.print("  LEN: "); Serial.print(msg.len);
      Serial.print(" DATA: ");
      for ( uint8_t i = 0; i < msg.len; i++ ) {
        Serial.print(msg.buf[i],HEX); Serial.print(" ");
      }
      Serial.println();
  }
  delay(1);
}*/


}

/*********************************************************************************************************
    END FILE
*********************************************************************************************************/
