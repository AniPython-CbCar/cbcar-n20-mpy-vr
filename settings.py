
# VR 手柄(LOOKBON) MAC 地址
BLE_MAC = "D5:51:FA:B6:09:71"  # 需要修改, 使用 test_get_mac_by_name.py 获取

# 是否反转, 如果电机方向反了, 可设置为 True
LEFT_REVERSE = False  # 左电机
RIGHT_REVERSE = False  # 右电机


# 设置开发板
BOARD = "ESP32-C3"  # ESP32-C3 或者 ESP32
if BOARD == "ESP32-C3":
    LED_PIN = 8
else:
    LED_PIN = 2  # ESP32

# 左电机
IN1 = 0
IN2 = 1

# 右电机
IN3 = 3
IN4 = 4


# 360度舵机
SERVO_PIN = 2


# 电机速度(0 ~ 1023)
MOTOR_SPEED_A = 220
MOTOR_SPEED_B = 500  # 默认
MOTOR_SPEED_C = 750
MOTOR_SPEED_D = 1000

# 舵机速度(0 ~ 100)
SERVO_SPEED = 26

# 设置手柄无通知超时, 自动关机
NO_NOTIFY_TIMEOUT = 5 # 分钟
