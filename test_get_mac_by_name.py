import ubluetooth
import time
from micropython import const

device_name = "LOOKBON"
is_find = False

# BLE 事件常量
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)


def decode_name(adv_data):
    """解析广播数据中的设备名"""
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


def decode_mac(addr):
    """将 addr 转换为标准 MAC 地址字符串"""
    return ":".join("{:02X}".format(b) for b in bytes(addr)).upper()


def bt_irq(event, data):
    global device_name, is_find

    if event == _IRQ_SCAN_RESULT:
        if is_find:
            return
        addr_type, addr, adv_type, rssi, adv_data = data
        mac_str = decode_mac(addr)
        name = decode_name(adv_data)
        print("发现设备:", mac_str, "名称:", name)
        if name and name.upper() == device_name.upper():
            device_name = name
            print("找到目标设备")
            print("*" * 20)
            print(mac_str)
            print("*" * 20)
            ble.gap_scan(None)  # 停止扫描
            is_find = True
    elif event == _IRQ_SCAN_DONE:
        if not is_find:
            ble.gap_scan(3000, 30000, 30000)


ble = ubluetooth.BLE()
ble.active(True)
ble.irq(bt_irq)

ble.gap_scan(5000, 30000, 30000)

while True:
    if is_find:
        break
    time.sleep(0.1)

