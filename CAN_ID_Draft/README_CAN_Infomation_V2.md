# Draft of Gachacon CAN Bus Protocol V2.1

# teTra Mk-7 SN2, SN1

## 1. I/O Control

### 0x1200, FET Controller
- CAN ID, 0x1200 - 0x120D
  - 0x1200: Serial number of GachaconECU No.0
  - 0x1201: Serial number of GachaconECU No.1
  - ......
  - 0x120D: Serial number of GachaconECU No.13
- Data, Range: 0x00 - 0xF0
  - 0x80: FET1 switch (ON:1, OFF:0)
  - 0x40: FET2 switch (ON:1, OFF:0)
- Response: TBD

### 0x1400, Output PWM
- CAN ID, 0x1400 - 0x140D (PWM No.1)
  - 0x1400: PWM No.1, Serial number of GachaconECU No.0
  - 0x1401: PWM No.1, Serial number of GachaconECU No.1
  - ......
  - 0x140D: PWM No.1, Serial number of GachaconECU No.13
- Data, Range: 0x0384 - 0x07D0 (900 - 2000)
  - requested output motor PWM, 900 - 2000 [usec]
- Response: TBD

### 0x1500
- Retired, GachaconECU only

### 0x1600, Relay Controller
- CAN ID, 0x1600 - 0x160D
  - 0x1600: Serial number of GachaconECU No.0
  - 0x1601: Serial number of GachaconECU No.1
  - ......
  - 0x160D: Serial number of GachaconECU No.13
- Data, Range: 0x00 - 0xF0
  - 0x80: Relay1 switch (ON:1, OFF:0)
  - 0x40: Relay2 switch (ON:1, OFF:0)
- Response: TBD

### 0x1700
- Retired, GachaconECU only

### 0x1800, Select PWM Controller
- CAN ID, 0x1800 - 0x180D
  - 0x1800: Serial number of GachaconECU No.0
  - 0x1801: Serial number of GachaconECU No.1
  - ......
  - 0x180D: Serial number of GachaconECU No.13
- Data, Range: 0x00 - 0xF0
  - 0x80: Select PWM1 (ON:1 and Other OFF, Default)
  - 0x40: Select PWM2 (ON:1 and Other OFF)
  - 0x20: Select PWM3 (ON:1 and Other OFF)
  - 0x10: Select PWM4 (ON:1 and Other OFF)
  - Other value -> 0x80
- Response: TBD

### 0x1900
- TBD

## 2. ESC-UART, information Voltage (Battery Voltage, Throttle, Act throttle, Bus current, Phase current)

### 0x1300, ESC-UART, Voltage
- CAN ID, 0x1300 - 0x130D
  - 0x1300: Serial number of GachaconECU No.0
  - 0x1301: Serial number of GachaconECU No.1
  - ......
  - 0x130D: Serial number of GachaconECU No.13
- Data, Ranage: 0x0000 - 0x01770 (0 - 0600)
  - Battery Voltage, 00.0 - 60.0 [V]

### 0x2000, ESC-UART, Throttle
- CAN ID, 0x2000 - 0x200D
  - 0x2000: Serial number of GachaconECU No.0
  - 0x2001: Serial number of GachaconECU No.1
  - ......
  - 0x200D: Serial number of GachaconECU No.13
- Data, Ranage:
  - Throttle

### 0x2100, ESC-UART, Act throttle
- CAN ID, 0x2100 - 0x210D
  - 0x2100: Serial number of GachaconECU No.0
  - 0x2101: Serial number of GachaconECU No.1
  - ......
  - 0x210D: Serial number of GachaconECU No.13
- Data, Ranage:
  - Act throttle

### 0x2200, ESC-UART, Bus current
- CAN ID, 0x2200 - 0x220D
  - 0x2200: Serial number of GachaconECU No.0
  - 0x2201: Serial number of GachaconECU No.1
  - ......
  - 0x220D: Serial number of GachaconECU No.13
- Data, Ranage:
  - Bus current

### 0x2300, ESC-UART, Phase current
- CAN ID, 0x2300 - 0x230D
  - 0x2300: Serial number of GachaconECU No.0
  - 0x2301: Serial number of GachaconECU No.1
  - ......
  - 0x230D: Serial number of GachaconECU No.13
- Data, Ranage:
  - Phase current



## 3. TBD



## 4. BMS information, BMS; Battery Management System

### 0x4000, Battery Voltage, Battery Current

### 0x4100, Cell Max/Min Voltage

### 0x4200, SoC, Duty, Flag (Discharge, Cell Balance)

### 0x4300, Temperature, Battery side Average/Max, BMS PCB side Average/Max

### 0x4400/0x4500, Each Cell Voltage

### 0x4600
- Retired, for using ENNOID BMS

### 0x4700
- Retired, for using ENNOID BMS

### 0x4800
- Retired, for using ENNOID BMS



## 5. TBD

## 6. TBD



## 7. redundant CAN

### 0x7000, switching and enable/disable CAN1(A)/CAN3(B)
- CAN ID, 0x7000 - 0x700D
  - 0x7000: Serial number of GachaconECU No.0
  - 0x7001: Serial number of GachaconECU No.1
  - ......
  - 0x700D: Serial number of GachaconECU No.13
- Data, Range: 0xA0 or 0x80 or 0x20
  - 0xA0: CAN1(A) ON  and CAN3(B) ON  (ON:1 and OFF:0, default)
  - 0x80: CAN1(A) ON  and CAN3(B) OFF (ON:1 and OFF:0)
  - 0x20: CAN1(A) OFF and CAN3(B) ON  (ON:1 and OFF:0) 
  - 0x00 or other: forbidden, hold previous state
- Response: No



## 8. Information, Warnning and Error code

### 0x8000, information of ECU Boot
- CAN ID, 0x8000 - 0x800D
  - 0x8000: Serial number of GachaconECU No.0
  - 0x8001: Serial number of GachaconECU No.1
  - ......
  - 0x800D: Serial number of GachaconECU No.13
- Data: A5
- Response: No

### 0x8100/0x8200 information of CAN BUS Health check
- CAN ID, 0x8100 - 0x810D
  - 0x8000: Serial number of GachaconECU No.0
  - 0x8001: Serial number of GachaconECU No.1
  - ......
  - 0x800D: Serial number of GachaconECU No.13
- Data: A5
- Response: Yes
- CAN ID, 0x8200 - 0x820D
  - 0x8200: Serial number of GachaconECU No.0
  - 0x8201: Serial number of GachaconECU No.1
  - ......
  - 0x820D: Serial number of GachaconECU No.13
- Data: 
  - Health Success: 5A
  - Health Fail: FF

### 0x8300/0x8400 information of CPU Temperature check
- CAN ID, 0x8300 - 0x830D
  - 0x8000: Serial number of GachaconECU No.0
  - 0x8001: Serial number of GachaconECU No.1
  - ......
  - 0x800D: Serial number of GachaconECU No.13
- Data: A5
- Response: Yes
- CAN ID, 0x8400 - 0x840D
  - 0x8200: Serial number of GachaconECU No.0
  - 0x8201: Serial number of GachaconECU No.1
  - ......
  - 0x820D: Serial number of GachaconECU No.13
- Data: 
  - Health Success: 5A
  - Health Fail: FF

### 0x8500 information of HV-Frame GND Leakage check

### 0x8600 information of LV-Frame GND Leakage check


