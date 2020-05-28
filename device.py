import time
from enum import Enum

from serial import Serial
from serial.tools import list_ports


CHANGE_MODE = ord('c')
AUDIO_LEVEL_MODE = ord('l')
DATA = ord('i')


class Device():

    class Status(Enum):
        DISCONNECTED = 0
        AUDIO_LEVEL_MODE = 1

    def __init__(self):
        self.serial = Serial()
        self.status = self.Status.DISCONNECTED

    def connect(self, port_idex, speed):
        self.serial.baudrate = speed()
        self.serial.port = list_ports.comports()[port_idex()].device
        self.serial.timeout = 0.005
        if self.serial.is_open:
            self.disconnect()
        self.serial.open()

    def disconnect(self):
        self.serial.close()

    def set_al_mode(self):
        self._write(CHANGE_MODE, AUDIO_LEVEL_MODE)
        self.status = self.Status.AUDIO_LEVEL_MODE

    def send_al_data(self, mono_fft, left_fft, right_fft):
        self._write(DATA, mono_fft, left_fft, right_fft)

    def _write(self, *data):
        if self.serial.is_open:
            data = [i if i < 255 else 255 for i in data]
            self.serial.reset_input_buffer()
            self.serial.write( b'p')
            if(self.serial.read(1) == b'c' ):
                print("c")
                self.serial.write(bytes(data))
            time.sleep(0.002)
            print(self.serial.read_all())


    # def set_color_pb_clic(ser: Serial):
    #     color = QColorDialog.getColor()
    #     if color.isValid():
    #         send_strep_color(ser, color)

    # def send_strep_color(ser: Serial, color: QColor):
    #     ser.write(bytes([ord("c"), color.red(),  color.green(), color.blue()]))