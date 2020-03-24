from time import sleep
import numpy as np
import pandas as pd
from rx.disposable import Disposable
from scipy import signal
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from rx.subject import BehaviorSubject

MIN_READ_BUFFER_DEPTH = 50
SAMPLING_RATE = 250
NUM_CHANNELS = 8

def notch(data, val=50, fs=SAMPLING_RATE):
    notch_freq_Hz = np.array([float(val)])
    for freq_Hz in np.nditer(notch_freq_Hz):
        bp_stop_Hz = freq_Hz + 3.0 * np.array([-1, 1])
        b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0), 'bandstop')
        fin = data = signal.lfilter(b, a, data, axis=0)
    return fin


def bandpass(data, start=5, stop=100, fs=SAMPLING_RATE):
    bp_Hz = np.array([start, stop])
    b, a = signal.butter(5, bp_Hz / (fs / 2.0), btype='bandpass')
    return signal.lfilter(b, a, data, axis=0)


class SensorSettings:
    simulation = True
    sensor_com_port = "/dev/ttyACM1"
    notch_filter = True
    bandpass_filter = True
    notch_frequency = 50
    bandpass_low_frequency = 5
    bandpass_high_frequency = 100
    amplitude_scale = 0.001


class SensorWrapper:
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    board_id = None
    board = None
    channels_idx = None
    buffer = None
    sensor_settings: SensorSettings = None
    rx_sensor_settings_subject_subscription: Disposable = None

    def __init__(self, rx_sensor_settings_subject: BehaviorSubject):
        self.sensor_settings = rx_sensor_settings_subject.value
        self.rx_sensor_settings_subject_subscription = rx_sensor_settings_subject.subscribe(self.set_sensor_settings)
        if self.sensor_settings.simulation:
            self.board_id = BoardIds.SYNTHETIC_BOARD.value
        else:
            self.board_id = BoardIds.CYTON_BOARD.value
            self.params.serial_port = self.sensor_settings.sensor_com_port
        self.board = BoardShim(self.board_id, self.params)
        self.channels_idx = BoardShim.get_emg_channels(self.board_id)
        self.buffer = np.empty([0, NUM_CHANNELS])
        self.board.prepare_session()
        self.board.start_stream()

    def set_sensor_settings(self, sensor_settings: SensorSettings):
        self.sensor_settings = sensor_settings

    def disconnect(self):
        self.board.stop_stream()
        self.board.release_session()
        self.rx_sensor_settings_subject_subscription.dispose()

    def read(self):
        data = self.board.get_board_data().transpose()[:, self.channels_idx]
        self.buffer = np.concatenate((self.buffer, data), axis=0)

    def read_filtered(self):
        self.read()
        if self.buffer.shape[0] < MIN_READ_BUFFER_DEPTH:
            return None
        read_matrix = np.asmatrix(self.buffer)
        self.buffer = np.empty([0, NUM_CHANNELS])
        if self.sensor_settings.notch_filter:
            read_matrix = np.apply_along_axis(notch, 0, read_matrix, val=self.sensor_settings.notch_frequency)[0]
        if self.sensor_settings.bandpass_filter:
            read_matrix = np.apply_along_axis(bandpass, 0, read_matrix, start=self.sensor_settings.bandpass_low_frequency,
                                          stop=self.sensor_settings.bandpass_high_frequency)
        return read_matrix


def main():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    sensor_wrapper = SensorWrapper(BehaviorSubject(SensorSettings()))
    sensor_wrapper.connect()
    sleep(5)
    data = sensor_wrapper.read_filtered()
    sensor_wrapper.disconnect()

    # demo how to convert it to pandas DF and plot data
    df = pd.DataFrame(data)
    print('Data From the Board')
    print(df.head(10))


if __name__ == "__main__":
    main()
