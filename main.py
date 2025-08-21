import time

from ble_controller import BLEController
from car import Motor, Servo360, Car
from conf import (BLE_MAC, IN1, IN2, IN3, IN4, SERVO_PIN,
                  LEFT_REVERSE, RIGHT_REVERSE, MOTOR_SPEED, SERVO_SPEED)

mo_a = Motor(IN1, IN2, reverse=LEFT_REVERSE)
mo_b = Motor(IN3, IN4, reverse=RIGHT_REVERSE)
servo = Servo360(SERVO_PIN)
car = Car(mo_a, mo_b, servo)


def handle_notify(key_hex):
    # print("===> 回调函数触发，按键值:", key_hex)

    # 方向键
    if key_hex == "D1":
        car.go(MOTOR_SPEED, MOTOR_SPEED),
    elif key_hex == "D2":
        car.go(-MOTOR_SPEED, -MOTOR_SPEED)
    elif key_hex == "D3":
        car.go(-MOTOR_SPEED, MOTOR_SPEED)
    elif key_hex == "D4":
        car.go(MOTOR_SPEED, -MOTOR_SPEED)
    elif key_hex == "D5":
        car.go(MOTOR_SPEED / 2, MOTOR_SPEED)
    elif key_hex == "D6":
        car.go(-MOTOR_SPEED / 2, -MOTOR_SPEED)
    elif key_hex == "D7":
        car.go(MOTOR_SPEED, MOTOR_SPEED / 2)
    elif key_hex == "D8":
        car.go(-MOTOR_SPEED, -MOTOR_SPEED / 2)
    elif key_hex == "D0":
        car.stop()

    # 舵机键
    # 1. 侧键上, 抬起
    elif key_hex == "A7":
        car.servo_speed(-SERVO_SPEED)
        time.sleep(0.56)
        car.servo_speed(0)
    elif key_hex == "B7":
        car.servo_speed(-SERVO_SPEED * 1.5)
    elif key_hex == "C7":
        car.servo_speed(0)

    # 2. 侧键下, 下降弹起
    elif key_hex == "A6":
        car.servo_speed(SERVO_SPEED)
        time.sleep(0.56)
        car.servo_speed(0)
    elif key_hex == "B6":
        car.servo_speed(SERVO_SPEED * 1.5)
    elif key_hex == "C6":
        car.servo_speed(0)


ble_controller = BLEController(BLE_MAC, notify_callback=handle_notify)
ble_controller.run()

