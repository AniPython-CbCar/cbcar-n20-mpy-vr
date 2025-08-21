# ble_controller.py
from machine import Pin, Timer
import ubluetooth
import time
from micropython import const
from ble_keymap import KEY_MAP
from conf import LED_PIN

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_NOTIFY = const(18)

class BLEController:
    # BLE 事件常量

    def __init__(self, target_mac, notify_callback=None):
        """
        target_mac: 目标设备的 MAC 地址
        notify_callback: 回调函数，格式 func(key_hex:str)
        """
        self.led = Pin(LED_PIN, Pin.OUT)
        self.timer = Timer(0)

        self.target_mac = target_mac.upper()
        self.device_name = None
        self.conn_handle = None
        self.target_to_connect = None
        self.notify_callback = notify_callback  # 保存回调函数

        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._bt_irq)

        self.led_blink()

    def led_on(self):
        if LED_PIN == 8:
            self.led.value(0)
        else:
            self.led.value(1)
        self.timer.deinit()

    def led_blink(self):
        self.timer.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

    def set_notify_callback(self, callback):
        """设置回调函数"""
        self.notify_callback = callback

    def decode_name(self, adv_data):
        adv_data = bytes(adv_data)
        n = 0
        while n + 1 < len(adv_data):
            length = adv_data[n]
            if length == 0:
                break
            type = adv_data[n + 1]
            if type == 0x09:  # Complete Local Name
                try:
                    return adv_data[n + 2:n + 1 + length].decode("utf-8")
                except UnicodeError:
                    return None
            n += 1 + length
        return None

    def decode_mac(self, addr):
        return ":".join("{:02X}".format(b) for b in bytes(addr))

    def start_scan(self):
        print("开始扫描目标设备...")
        self.ble.gap_scan(5000, 30000, 30000)

    def _bt_irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            mac_str = self.decode_mac(addr)
            name = self.decode_name(adv_data)
            print("发现设备:", mac_str, "名称:", name)
            if mac_str == self.target_mac:
                self.device_name = name
                print("找到目标设备:", mac_str, "名称:", self.device_name)
                self.ble.gap_scan(None)  # 停止扫描
                self.target_to_connect = (addr_type, bytes(addr))

        elif event == _IRQ_SCAN_DONE:
            if self.conn_handle is None and self.target_to_connect is None:
                self.start_scan()

        elif event == _IRQ_PERIPHERAL_CONNECT:
            self.conn_handle, addr_type, addr = data
            print("连接成功:", self.decode_mac(addr))
            print("设备名称:", self.device_name)
            self.led_on()

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            self.led_blink()
            self.conn_handle, addr_type, addr = data
            print("连接断开:", self.decode_mac(addr))
            self.device_name = None
            self.conn_handle = None
            self.start_scan()
            time.sleep(3)

        elif event == _IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            key_hex = notify_data.hex().upper()
            # print("收到通知数据:", key_hex)

            # 如果有映射表，打印解析结果
            if key_hex in KEY_MAP:
                # print("解析结果:", KEY_MAP[key_hex])
                # 调用用户自定义回调
                if self.notify_callback:
                    self.notify_callback(key_hex)
            else:
                print("未知按键:", key_hex)


    def run(self):
        self.start_scan()
        while True:
            if self.target_to_connect:
                addr_type, addr = self.target_to_connect
                print("尝试连接设备:", self.decode_mac(addr))
                self.ble.gap_connect(addr_type, addr)
                self.target_to_connect = None
            time.sleep(1)


if __name__ == "__main__":
    def handle_notify(key_hex):
        print("===> 回调函数触发，按键值:", key_hex)

    TARGET_MAC  = "D5:51:FA:B6:09:71"  # 替换为目标设备的 MAC 地址
    ble_controller = BLEController(TARGET_MAC, notify_callback=handle_notify)
    ble_controller.run()
