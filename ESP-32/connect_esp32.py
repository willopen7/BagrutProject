# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/micropython-esp32-bluetooth-low-energy-ble/

from micropython import const
import asyncio
import aioble
import bluetooth
import struct
from machine import Pin, UART
from random import randint
from brain import Brain
import time

# Init LED
# led = Pin(2, Pin.OUT)
# led.value(0)
# Init random value
value = 0

# See the following for generating UUIDs:
# https://www.uuidgenerator.net/
_BLE_SERVICE_UUID = bluetooth.UUID('19b10000-e8f2-537e-4f6c-d104768a1214')
_BLE_FOCUS_CHAR_UUID =bluetooth.UUID('1a9fa98f-45ae-4453-b95f-08cb978aa29d')
_BLE_CALM_CHAR_UUID = bluetooth.UUID('19b10001-e8f2-537e-4f6c-d104768a1214')
_BLE_LED_UUID = bluetooth.UUID('19b10002-e8f2-537e-4f6c-d104768a1214')
# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

brain_module = Brain(2)

# Register GATT server, the service and characteristics
ble_service = aioble.Service(_BLE_SERVICE_UUID)
focus_characteristic = aioble.Characteristic(ble_service, _BLE_FOCUS_CHAR_UUID, read=True, notify=True)
calm_characteristic = aioble.Characteristic(ble_service, _BLE_CALM_CHAR_UUID, read=True, notify=True)
led_characteristic = aioble.Characteristic(ble_service, _BLE_LED_UUID, read=True, write=True, notify=True, capture=True)

# Register service(s)
aioble.register_services(ble_service)

# Helper to encode the data characteristic UTF-8
def _encode_data(data):
    return str(data).encode('utf-8')

# Helper to decode the LED characteristic encoding (bytes).
def _decode_data(data):
    try:
        if data is not None:
            # Decode the UTF-8 data
            number = int.from_bytes(data, 'big')
            return number
    except Exception as e:
        print("Error decoding temperature:", e)
        return None

# Get sensor readings
def get_random_value():
    return randint(0,100)

# Get new value and update characteristic
async def sensor_task():
    while True:
        brain_module.update()
        debug_info = brain_module.debug_info  # ✅ Read debug data

        print(f"🚀 Packet Length: {debug_info.get('packet_length', 'N/A')}")  
        print(f"🚀 First Full Packet: {debug_info.get('first_packet', [])}")  
        print(f"🚀 Last Byte Read (Checksum): {debug_info.get('last_byte_read', 'N/A')}")  # ✅ Ensure it's not N/A
        print(f"Checksum Valid: {debug_info['checksum_valid']}")
        print(f"Expected: {debug_info['checksum_expected']}, Got: {debug_info['checksum_got']}")
        print(f"Checksum Accumulator: {debug_info['checksum_accumulator']}")  

        print("All stats:", brain_module.read_csv())  
        await asyncio.sleep_ms(500)
        
# Serially wait for connections. Don't advertise while a central is connected.
async def peripheral_task():
    while True:
        try:
            async with await aioble.advertise(
                _ADV_INTERVAL_MS,
                name="ESP32",
                services=[_BLE_SERVICE_UUID],
                ) as connection:
                    print("Connection from", connection.device)
                    await connection.disconnected()             
        except asyncio.CancelledError:
            # Catch the CancelledError
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in peripheral_task:", e)
        finally:
            # Ensure the loop continues to the next iteration
            await asyncio.sleep_ms(100)

async def wait_for_write():
    while True:
        try:
            connection, data = await led_characteristic.written()
            print(data)
            print(type)
            data = _decode_data(data)
            print('Connection: ', connection)
            print('Data: ', data)
            if data == 1:
                print('Turning LED ON')
                led.value(1)
            elif data == 0:
                print('Turning LED OFF')
                led.value(0)
            else:
                print('Unknown command')
        except asyncio.CancelledError:
            # Catch the CancelledError
            print("Peripheral task cancelled")
        except Exception as e:
            print("Error in peripheral_task:", e)
        finally:
            # Ensure the loop continues to the next iteration
            await asyncio.sleep_ms(100)
            
# dRun tasks
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    t3 = asyncio.create_task(wait_for_write())
    await asyncio.gather(t1, t2)
    
asyncio.run(main())
