from PyQt5 import QtWidgets
from serial.tools import list_ports

from conf import Configs

INDEX = "index"

configs = Configs()


def set_combobox_index(combo_box: QtWidgets.QToolBox):
    try:
        if (int(configs.load_state_value(combo_box.objectName(), INDEX)) < combo_box.count()):
            combo_box.setCurrentIndex(int(configs.load_state_value(combo_box.objectName(), INDEX)))
    except ValueError:
        configs.save_state_value(combo_box.objectName(), INDEX, str(combo_box.currentIndex()))


def save_combobox_index(combo_box: QtWidgets.QToolBox):
    configs.save_state_value(combo_box.objectName(), INDEX, str(combo_box.currentIndex()))

def get_com_ports():
    return [f"{item.device} - {item.manufacturer}" for item in list_ports.comports()]



