"""
两个马达 + 360 度舵机的小车类
"""

import time
from machine import Pin, PWM


def limit_value(value, min_value=0, max_value=1023):
    return max(min_value, min(max_value, value))


class Motor:
    def __init__(self, in1, in2, reverse=False, duty_offset=0):
        """初始化马达对象"""
        self.pwm1 = PWM(Pin(in1), freq=1000, duty_u16=0)
        self.pwm2 = PWM(Pin(in2), freq=1000, duty_u16=0)
        self.duty_offset = duty_offset
        self.reverse = reverse

    def start(self, speed):
        """启动马达并设置速度 (-1023 ~ 1023)"""
        if speed == 0:
            self.stop()
            return

        if self.reverse:
            speed = -speed

        en = int(limit_value(abs(speed) + self.duty_offset))

        if speed > 0:
            self.pwm1.duty(0)
            self.pwm2.duty(en)
        else:
            self.pwm1.duty(en)
            self.pwm2.duty(0)

    def stop(self):
        """停止马达"""
        self.pwm1.duty(0)
        self.pwm2.duty(0)


class Servo360:
    def __init__(self, pin, freq=50, mid=4915):
        """初始化 360 度舵机
        pin: 舵机控制引脚
        freq: 50Hz (标准舵机)
        """
        self.pwm = PWM(Pin(pin), freq=freq)
        self.mid = mid
        self.stop()

    def speed(self, value):
        """设置舵机转速
        value: -100 ~ 100   (负数反转, 正数正转, 0 停止)
        """
        value = max(-100, min(100, value))  # 限制范围
        # duty 范围: 假设 duty_u16(0-65535), 中值≈4915 (≈1.5ms)
        delta = int(2000 * value / 100)  # 最大偏移量可调
        self.pwm.duty_u16(self.mid + delta)

    def stop(self):
        """停止舵机"""
        self.pwm.duty_u16(self.mid)  # 中值 = 停止


class Car:
    def __init__(self, motor_a, motor_b, servo=None):
        """初始化汽车对象"""
        self.motor_a = motor_a
        self.motor_b = motor_b
        self.servo = servo  # 可选的 360 度舵机

    def go(self, speed_a, speed_b):
        """启动汽车马达"""
        self.motor_a.start(speed_a)
        self.motor_b.start(speed_b)

    def stop(self):
        """停止汽车"""
        self.motor_a.stop()
        self.motor_b.stop()
        if self.servo:
            self.servo.stop()
        # print("汽车停止")

    def servo_speed(self, value):
        """控制 360 度舵机转速"""
        if self.servo:
            self.servo.speed(value)


def test_motor(in1, in2, in3, in4):
    """测试小车和舵机"""
    mo_a = Motor(in1, in2, reverse=False)
    mo_b = Motor(in3, in4, reverse=False)
    car = Car(mo_a, mo_b, servo=None)

    en = 300
    # 前进
    car.go(en, en)
    time.sleep(1)
    # 后退
    car.go(-en, -en)
    time.sleep(1)
    # 左转
    car.go(-en, en)
    time.sleep(1)
    # 右转
    car.go(en, -en)
    time.sleep(1)

    # 停止
    car.stop()

def test_servo(pin):
    """测试舵机"""
    speed = 20
    servo = Servo360(pin)  # 假设 360 度舵机接 GPIO25
    servo.speed(speed)
    time.sleep(2)
    # servo.speed(-speed)
    # time.sleep(2)
    # servo.speed(0)  # 停止舵机


if __name__ == "__main__":
    # test_motor(0, 1, 5, 7)
    while True:
        test_servo(6)
