# test_pwm_manual_mode_motor_run
# can1とcan0とcan2は接続に合わせてくれ
# 800モーターストップ -> 0x0320
# 1200モーター回る -> 0x04b0

cansend can1 00001401#04b0
cansend can1 00001402#04b0
cansend can1 00001403#04b0
cansend can1 00001404#04b0
cansend can1 00001405#04b0
cansend can1 00001406#04b0

cansend can0 00001407#04b0
cansend can0 00001408#04b0
cansend can0 00001409#04b0
cansend can0 0000140A#04b0
cansend can0 0000140B#04b0
cansend can0 0000140C#04b0


