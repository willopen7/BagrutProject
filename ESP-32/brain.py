from machine import UART

print("yop")
class Brain:
    MAX_PACKET_LENGTH = 32
    EEG_POWER_BANDS = 8

    def __init__(self, uart_port, baud_rate=9600):
        # Initialize UART
        self.uart = UART(uart_port, baudrate=baud_rate)

        # Initialization of variables
        self.fresh_packet = False
        self.in_packet = False
        self.packet_index = 0
        self.packet_length = 0
        self.checksum = 0
        self.checksum_accumulator = 0
        self.has_power = False

        self.signal_quality = 200
        self.attention = 0
        self.meditation = 0

        self.packet_data = [0] * self.MAX_PACKET_LENGTH
        self.eeg_power = [0] * self.EEG_POWER_BANDS
        self.latest_error = ""
        self.latest_byte = None
        self.last_byte = None

    def get_debug_info(self):
        return {
            "latest_byte": self.latest_byte,
            "packet_index": self.packet_index,
            "packet_length": self.packet_length,
            "checksum": self.checksum,
            "error": self.latest_error
        }

    def update(self):
        parse_return = 0
        print("here")
        if self.uart.any():
            print("UART Data Available")
            self.latest_byte = self.uart.read(1)[0]
            print("Latest Byte Read:", self.latest_byte)

            # Build a packet
            if self.in_packet:
                if self.packet_index == 0:
                    self.packet_length = self.latest_byte
                    if self.packet_length > self.MAX_PACKET_LENGTH:
                        self.latest_error = "ERROR: Packet too long"
                        self.in_packet = False
                elif self.packet_index <= self.packet_length:
                    self.packet_data[self.packet_index - 1] = self.latest_byte
                    self.checksum_accumulator += self.latest_byte
                else:
                    self.checksum = self.latest_byte
                    self.checksum_accumulator = 255 - self.checksum_accumulator
                    if self.checksum == self.checksum_accumulator:
                        parse_return = self.parse_packet()
                        if parse_return > 0:
                            self.fresh_packet = True
                        else:
                            self.latest_error = "ERROR: Could not parse"
                    else:
                        self.latest_error = "ERROR: Checksum"
                    self.in_packet = False

                self.packet_index += 1

            # Look for the start of the packet
            if self.latest_byte == 170 and self.last_byte == 170 and not self.in_packet:
                self.in_packet = True
                self.packet_index = 0
                self.packet_length = 0
                self.checksum = 0
                self.checksum_accumulator = 0

            self.last_byte = self.latest_byte

        if self.fresh_packet:
            self.fresh_packet = False
            return parse_return
        else:
            return 0

    def clear_eeg_power(self):
        self.eeg_power = [0] * self.EEG_POWER_BANDS

    def parse_packet(self):
        self.has_power = False
        self.clear_eeg_power()
        return_byte = 0x0

        i = 0
        while i < self.packet_length:
            data = self.packet_data[i]
            if data == 0x02:
                i += 1
                self.signal_quality = self.packet_data[i]
                return_byte |= 0b00000001
            elif data == 0x04:
                i += 1
                self.attention = self.packet_data[i]
                return_byte |= 0b00000010
            elif data == 0x05:
                i += 1
                self.meditation = self.packet_data[i]
                return_byte |= 0b00000100
            elif data == 0x83:
                i += 1
                for j in range(self.EEG_POWER_BANDS):
                    self.eeg_power[j] = (
                            (self.packet_data[i] << 16)
                            | (self.packet_data[i + 1] << 8)
                            | self.packet_data[i + 2]
                    )
                    i += 3
                self.has_power = True
                return_byte |= 0b00001000
            elif data == 0x80:
                i += 1
                self.raw_value = (self.packet_data[i] << 8) | self.packet_data[i + 1]
                i += 1
                return_byte |= 0b00010000
            else:
                return 0x0
            i += 1

        return return_byte

    def read_errors(self):
        return self.latest_error

    def read_signal_quality(self):
        return self.signal_quality

    def read_attention(self):
        return self.attention

    def read_meditation(self):
        return self.meditation

    def read_power_array(self):
        return self.eeg_power

    def read_csv(self):
        if self.has_power:
            return "{},{},{},{}".format(
                self.signal_quality,
                self.attention,
                self.meditation,
                ",".join(map(str, self.eeg_power)),
            )
        else:
            return "{},{},{}".format(self.signal_quality, self.attention, self.meditation)
