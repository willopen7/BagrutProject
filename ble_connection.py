# ble_connection.py
import asyncio
from ble_module import BLEModule
from bleak import BleakClient

NAME = "ESP32"


# BLE logic in a separate function
async def ble_logic(name):
    ble = BLEModule()
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
        val = await ble.read_characteristic('19b10002-e8f2-537e-4f6c-d104768a1214')
        await ble.write_characteristic('19b10002-e8f2-537e-4f6c-d104768a1214', bytes([0]))
        print(val)


# BLE thread starter
def start_ble_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ble_logic(NAME))
