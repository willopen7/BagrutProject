# ble_connection.py
import asyncio
from ble_module import BLEModule
from bleak import BleakClient

NAME = "ESP32"
BLE_FOCUS_UUID = "1a9fa98f-45ae-4453-b95f-08cb978aa29d"
BLE_CALM_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
ble = BLEModule()
focus_val = 0
calm_val = 0
should_stop = False


def get_focus_and_calm():
    return focus_val, calm_val


def stop_ble():
    global should_stop
    should_stop = True


# BLE logic in a separate function
async def ble_logic(name):
    global ble, focus_val, calm_val
    devices = await ble.scan_devices()
    print("Found devices:", devices)
    if devices:
        found_device = False
        connected = False
        led_uuid = '19b10000-e8f2-537e-4f6c-d104768a1214'
        for d in devices:
            if d[0] == name:
                connected = await ble.connect_device(d[1]) # Connect to the first device
                found_device = True
                break
        if not found_device:
            connected = await ble.connect_device(devices[0][1])
        await ble.print_services_and_characteristics()
        while not should_stop:
            try:
                focus = await ble.read_characteristic(BLE_FOCUS_UUID)
                calm = await ble.read_characteristic(BLE_CALM_UUID)
                focus_val = int(focus.decode('utf-8'))
                calm_val = int(calm.decode('utf-8'))
                print(focus_val, calm_val)
            except Exception as e:
                print("Error reading characteristics:", e)
            await asyncio.sleep(1)


# BLE thread starter
def start_ble_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ble_logic(NAME))
