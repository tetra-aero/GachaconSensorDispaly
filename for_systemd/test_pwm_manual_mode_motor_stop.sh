# test_pwm_manual_mode_motor_run
# can1とcan0とcan2は接続に合わせてくれ
# 800モーターストップ -> 0x0320
# 1200モーター回る -> 0x04b0
# 1300モーター回る -> 0x04c0

cansend can1 00001401#0320
cansend can1 00001402#0320
cansend can1 00001403#0320
cansend can1 00001404#0320
cansend can1 00001405#0320
cansend can1 00001406#0320

cansend can0 00001407#0320
cansend can0 00001408#0320
cansend can0 00001409#0320
cansend can0 0000140A#0320
cansend can0 0000140B#0320
cansend can0 0000140C#0320
