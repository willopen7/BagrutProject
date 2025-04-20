import asyncio
import aioble
import bluetooth
from brain import Brain
import time

_BLE_SERVICE_UUID = bluetooth.UUID('19b10000-e8f2-537e-4f6c-d104768a1214')
_BLE_FOCUS_CHAR_UUID =bluetooth.UUID('1a9fa98f-45ae-4453-b95f-08cb978aa29d')
_BLE_CALM_CHAR_UUID = bluetooth.UUID('19b10001-e8f2-537e-4f6c-d104768a1214')
# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

brain_module = Brain(2)

# Register GATT server, the service and characteristics
ble_service = aioble.Service(_BLE_SERVICE_UUID)
focus_characteristic = aioble.Characteristic(ble_service, _BLE_FOCUS_CHAR_UUID, read=True, notify=True)
calm_characteristic = aioble.Characteristic(ble_service, _BLE_CALM_CHAR_UUID, read=True, notify=True)

# Register service(s)
aioble.register_services(ble_service)

# Helper to encode the data characteristic UTF-8
def _encode_data(data):
    return str(data).encode('utf-8')

# Get new value and update characteristic
async def sensor_task():
    while True:
        packet = brain_module.read_packet()
        attention = brain_module.get_attention(packet)
        meditation = brain_module.get_meditation(packet)
        focus_characteristic.write(_encode_data(attention), send_update=True)
        calm_characteristic.write(_encode_data(meditation), send_update=True)
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
            
# Run tasks
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)
    
asyncio.run(main())
