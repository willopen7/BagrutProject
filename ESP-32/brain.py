from machine import UART, Pin
import time
    
    
class Brain:
    def __init__(self, uart_port, baud_rate=9600):
        self.uart = UART(uart_port, baudrate=baud_rate)
    
    def remain_in_bounds(self, val: int, min_val: int, max_val: int):
        ret = max(min(val, max_val), min_val)
        return ret

    def calculate_wave_data(self, data: List):
        if len(data) < 3:
            return -1
        return ((data[0] << 16) + (data[1] << 8) + data[2])
    
    def read_packet(self):
        ret = []
        while True:
            if self.uart.any():
                data = ord(self.uart.read(1))
                if data == 170:
                    if self.uart.any():
                        if ord(self.uart.read(1)) == 170:
                            return ret
                else:
                    ret.append(data)   
            time.sleep(0.01)
            
    def get_attention(self, packet):
        beta = self.calculate_wave_data(packet[19:22]) + self.calculate_wave_data(packet[22:25])
        theta = self.calculate_wave_data(packet[10:13])
        if theta == 0:
            raw_value = beta / (theta + 1)
        else:
            raw_value = beta / theta
        return self.remain_in_bounds(int((raw_value/15) * 100), 1, 100)
    
    def get_meditation(self, packet):
        beta = self.calculate_wave_data(packet[19:22]) + self.calculate_wave_data(packet[22:25])
        alpha = self.calculate_wave_data(packet[13:16]) + self.calculate_wave_data(packet[16:19])
        if beta == 0:
            raw_value = alpha / (beta + 1)
        else:
            raw_value = alpha / beta
        return self.remain_in_bounds(int((raw_value/2.5) * 100), 1, 100)
    