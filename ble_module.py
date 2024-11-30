# ble_module.py
from bleak import BleakScanner, BleakClient


class BLEModule:
    def __init__(self):
        self.client = None

    async def scan_devices(self):
        devices = await BleakScanner.discover()
        return [(d.name, d.address) for d in devices]

    async def connect_device(self, address):
        self.client = BleakClient(address)
        await self.client.connect()
        print(address)
        return self.client.is_connected

    async def disconnect_device(self):
        if self.client:
            await self.client.disconnect()
            self.client = None

    async def read_characteristic(self, char_uuid):
        if self.client:
            return await self.client.read_gatt_char(char_uuid)
        raise RuntimeError("No connected client")

    async def write_characteristic(self, char_uuid, data):
        if self.client:
            await self.client.write_gatt_char(char_uuid, data)
        else:
            raise RuntimeError("No connected client")

    async def print_services_and_characteristics(self):
        """Print all services and characteristics of the BLE device."""
        if not self.client or not self.client.is_connected:
            raise Exception("Client is not connected.")

        services = self.client.services
        for service in services:
            print(f"- Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  - Characteristic: {char.uuid} (Properties: {char.properties})")
