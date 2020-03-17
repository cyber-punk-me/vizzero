import sys
import traceback

sys.path.append('file')
sys.path.append('sensor')
from sensor.sensor_wrapper import *
import serial.tools.list_ports
from file.fileUtil import *
from PySide2.QtWidgets import QPushButton
import threading
from rx.subject import Subject, BehaviorSubject


class FileController:
    file_writer = None

    def start_file(self, dir, name):
        self.file_writer = FileWriter(dir, name.name)
        self.file_writer.start_file()

    def append_data(self, data):
        self.file_writer.append_data(data)

    def finish_file(self):
        if self.file_writer is not None:
            self.file_writer.finish_file()
            self.file_writer = None

    def delete_latest_file(self):
        self.file_writer.delete_latest_file()


class DataThread(threading.Thread):
    sensor = None
    data_running = True
    rx_sensor_data_subject = None
    rx_sensor_settings_subject = None

    def __init__(self, rx_sensor_data_subject, rx_sensor_settings_subject):
        super(DataThread, self).__init__()
        self.sensor = None
        self.rx_sensor_data_subject = rx_sensor_data_subject
        self.rx_sensor_settings_subject = rx_sensor_settings_subject

    def stop(self):
        self.data_running = False

    def run(self):
        self.sensor = SensorWrapper(self.rx_sensor_settings_subject)
        try:
            while self.data_running:
                data = self.sensor.read_filtered()
                if data is not None:
                    self.rx_sensor_data_subject.on_next(data)
                sleep(0.01)
        except Exception:
            traceback.print_exc(file=sys.stdout)
        finally:
            self.sensor.disconnect()


class SensorController:
    rx_sensor_data_subject = None
    rx_sensor_settings_subject = None
    data_thread = None

    def __init__(self):
        self.rx_sensor_data_subject = Subject()
        self.rx_sensor_settings_subject = BehaviorSubject(SensorSettings())

    def start_data(self):
        if self.data_thread is None:
            self.data_thread = DataThread(self.rx_sensor_data_subject, self.rx_sensor_settings_subject)
            self.data_thread.start()

    def stop_data(self):
        if self.data_thread is not None:
            self.data_thread.stop()
            self.data_thread = None

    def sensor_connected(self):
        return self.data_thread is not None

    def update_sensor_settings(self, sensor_settings: SensorSettings):
        self.rx_sensor_settings_subject.on_next(sensor_settings)

    def list_serial_ports(self):
        return [comport.device for comport in serial.tools.list_ports.comports()]


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

    def write_to_file(self, dir, file_name):
        if self.file_sensor_subs is None:
            self.file_controller.start_file(dir, file_name)
            self.file_sensor_subs = self.sensor_controller.rx_sensor_data_subject.subscribe(
                self.file_controller.append_data)

    def finish_file(self):
        if self.file_sensor_subs is not None:
            self.file_sensor_subs.dispose()
            self.file_sensor_subs = None
            self.file_controller.finish_file()


class BasePlugin:
    core_controller = None

    def __init__(self, core_controller=None):
        self.core_controller = core_controller

    def create_widget(self, parent=None):
        return QPushButton('Dummy widget')

    def destroy(self):
        pass

    def get_name(self):
        return ""
