import functools
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from serial import SerialBase

import conf
import device
from input.portaudio import Portrecorder as Recorder
# from input.portaudio import Portrecorder as Recorder
# from process.audio_processor import AudioProcessor
from process.audio_processor import AudioProcessor
from utils import set_combobox_index, save_combobox_index, get_com_ports
from window.untitled import Ui_MainWindow

spc = None  # serial port connection


class MyWindow(QMainWindow):

    def __init__(self):
        self.close_functions = []
        super().__init__()

    def closeEvent(self, *args, **kwargs):  # real signature unknown
        for fun in self.close_functions:
            fun()

    def updateStacked(self, row):
        self.sw_mode.setCurrentIndex(row)



if __name__ == '__main__':

    configs = conf.Configs()
    # app = QtWidgets.QApplication(sys.argv)
    app = QtWidgets.QApplication([])
    window = MyWindow()
    win = Ui_MainWindow()
    win.setupUi(window)
    # win = uic.loadUi("window/untitled.ui")
    device = device.Device()

    win.lw_modes.currentRowChanged.connect(win.sw_mode.setCurrentIndex)

    win.com_ports.addItems(get_com_ports())
    set_combobox_index(win.com_ports)
    win.com_ports.currentIndexChanged.connect(functools.partial(save_combobox_index, win.com_ports))
    win.com_speeds.addItems([str(elem) for elem in SerialBase.BAUDRATES])
    set_combobox_index(win.com_speeds)
    win.com_speeds.currentIndexChanged.connect(functools.partial(save_combobox_index, win.com_speeds))

    # win.com_speeds.setCurrentIndex(tuple.index(SerialBase.BAUDRATES, 9600))
    win.pb_connect.clicked.connect(functools.partial(device.connect, lambda: win.com_ports.currentIndex(), lambda: win.com_speeds.currentText()))
    win.pb_disconnect.clicked.connect(lambda: device.disconnect())
    window.close_functions.append(lambda: device.disconnect())

    win.setAlMod.clicked.connect(device.set_al_mode)
    # win.set_color_pb.clicked.connect(functools.partial(set_color_pb_clic, serial))

    window.show()

    recorder = Recorder(
        chunks=configs.settings.getint('recorder', 'chunks'),
        chunksize=configs.settings.getint('recorder', 'chunksize'),
        channels=configs.settings.getint('recorder', 'channels'),
        rate=configs.settings.get('recorder', 'rate'),
    )

    audio_processor = AudioProcessor(
        configs,
        chunks=recorder.elements_per_ringbuffer,
        chunksize=recorder.frames_per_element,
        channels=recorder.channels,
        rate=recorder.rate,
    )

    recorder.start()

    def update():
        """Pass data from recorder via processor to visualizer."""
        # while True:
        if recorder.has_new_audio:
            audio_processor.set_audio(recorder.ringbuffer)
            audio_lavels = [audio_processor.rms_mono(), *audio_processor.rms_stereo()]
            audio_lavels = [int(i/win.gain.value()  ) for i in audio_lavels]


            win.general.setValue(audio_lavels[0])
            win.right.setValue(audio_lavels[1])
            win.left.setValue(audio_lavels[2])

            if device.status is device.Status.AUDIO_LEVEL_MODE:
                device.send_al_data(*audio_lavels)
                # device.status = device.Status.DISCONNECTED
            # await asyncio.sleep(0.20)
            # fft_amplitudes = audio_processor.log_frequency_spectrum()
            # pen = pg.mkPen(color='r')
            # win.graphicsView.plot(list(range(577)), fft_amplitudes, pen=pen, clear=True)
            # visualizer.set_data(fft_amplitudes)
        # pg.QtCore.QTimer.singleShot(1, update)


    # update()

    # ioloop = asyncio.get_event_loop()
    # task = ioloop.create_task(update())
    # task = asyncio.create_task(update())
    # task.start()

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1000/100)






    sys.exit(app.exec())

