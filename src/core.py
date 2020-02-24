import sys
import traceback

sys.path.append('file')
sys.path.append('sensor')
from sensor.sensorwrapper import *
from file.fileUtil import *
from PySide2.QtWidgets import QPushButton
import threading
from rx.subject import Subject


class FileController:
    file_writer = None

    def start_file(self, name):
        self.file_writer = FileWriter(name)

    def append_data(self, data):
        self.file_writer.append_data(data)

    def finish_file(self):
        self.file_writer.finish_file()
        self.file_writer = None

    def delete_latest_file(self):
        self.file_writer.delete_latest_file()


class DataThread(threading.Thread):
    sensor = None
    data_running = True
    rx_subject = None

    def __init__(self, rx_subject):
        super(DataThread, self).__init__()
        self.sensor = None
        self.rx_subject = rx_subject

    def stop(self):
        self.data_running = False

    def run(self):
        self.sensor = SensorWrapper()
        self.sensor.connect()
        try:
            while self.data_running:
                data = self.sensor.read_filtered()
                if data is not None:
                    self.rx_subject.on_next(data)
        except Exception:
            traceback.print_exc(file=sys.stdout)
        finally:
            self.sensor.disconnect()


class SensorController:
    rx_sensor_data_subject = None
    data_thread = None

    def __init__(self):
        self.rx_sensor_data_subject = Subject()

    def start_data(self):
        if self.data_thread is None:
            self.data_thread = DataThread(self.rx_sensor_data_subject)
            self.data_thread.start()

    def stop_data(self):
        if self.data_thread is not None:
            self.data_thread.stop()
            self.data_thread = None


class CoreController:
    file_controller = None
    sensor_controller = None
    file_sensor_subs = None

    def __init__(self):
        self.file_controller = FileController()
        self.sensor_controller = SensorController()

    def start_data(self):
        self.sensor_controller.start_data()

    def stop_data(self):
        self.sensor_controller.stop_data()

    def write_to_file(self, file_name):
        if self.file_sensor_subs is None:
            self.file_controller.start_file(file_name)
            self.file_sensor_subs = self.sensor_controller.rx_sensor_data_subject.subscribe(self.file_controller.append_data)

    def finish_file(self):
        if self.file_sensor_subs is not None:
            self.sensor_controller.rx_sensor_data_subject.dispose()
            self.file_controller.finish_file()
            self.file_sensor_subs = None


class BasePlugin:
    core_controller = None

    def __init__(self, core_controller=None):
        self.core_controller = core_controller

    def create_widget(self):
        return QPushButton('Dummy widget')
