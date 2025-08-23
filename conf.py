# 设置开发板
BOARD = "ESP32-C3"  # ESP32-C3 或者 ESP32

# VR 手柄(LOOKBON) MAC 地址
# BLE_MAC = "9A:E3:4F:3E:F2:BF"  # 根据实际情况修改
BLE_MAC = "D5:51:FA:B6:09:71"  # 白VR

if BOARD == "ESP32-C3":
    LED_PIN = 8
else:
    LED_PIN = 2  # ESP32

# 左电机
IN1 = 0
IN2 = 1

# 右电机
IN3 = 5
IN4 = 7


# 360度舵机
SERVO_PIN = 6

# 是否反转
LEFT_REVERSE = True  # 左电机
RIGHT_REVERSE = False  # 右电机


# 电机速度(0 ~ 1023)
MOTOR_SPEED_A = 250
MOTOR_SPEED_B = 500  # 默认
MOTOR_SPEED_C = 750
MOTOR_SPEED_D = 1000

# 舵机速度(0 ~ 100)
SERVO_SPEED = 30
SERVO_SPEED_MAX = 36
