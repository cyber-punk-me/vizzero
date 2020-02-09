import argparse
from time import sleep
import numpy as np
import pandas as pd
from scipy import signal

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

READ_BUFFER_DEPTH = 50
SAMPLING_RATE = 250

def notch(data, val=50, fs=SAMPLING_RATE):
    notch_freq_Hz = np.array([float(val)])
    for freq_Hz in np.nditer(notch_freq_Hz):
        bp_stop_Hz = freq_Hz + 3.0 * np.array([-1, 1])
        b, a = signal.butter(3, bp_stop_Hz / (fs / 2.0), 'bandstop')
        fin = data = signal.lfilter(b, a, data)
    return fin


def bandpass(data, start=5, stop=100, fs=SAMPLING_RATE):
    bp_Hz = np.array([start, stop])
    b, a = signal.butter(5, bp_Hz / (fs / 2.0), btype='bandpass')
    return signal.lfilter(b, a, data, axis=0)


class SensorWrapper:
    BoardShim.enable_dev_board_logger()
    params = BrainFlowInputParams()
    board_id = None
    board = None
    channels_idx = None
    buffer = None
    time_to_fill_buffer = READ_BUFFER_DEPTH / SAMPLING_RATE / 1000

    def __init__(self, address='', sim=True):
        if sim:
            self.board_id = BoardIds.SYNTHETIC_BOARD.value
        else:
            # todo board port
            self.board_id = BoardIds.CYTON_BOARD.value
        self.board = BoardShim(self.board_id, self.params)
        self.channels_idx = BoardShim.get_emg_channels(self.board_id)
        self.buffer = np.empty([1, 8])

    def connect(self):
        self.board.prepare_session()
        self.board.start_stream()

    def disconnect(self):
        self.board.stop_stream()
        self.board.release_session()

    def read(self):
        data = self.board.get_board_data().transpose()[:, self.channels_idx]
        return data

    def fill_read_buffer(self, retry=10):
        data = self.read()
        while retry > 0 and self.buffer.shape[1] < READ_BUFFER_DEPTH:
            # we should wait time to fill buffer,
            # but gonna read 5 times more
            # often and rely on retry
            sleep(self.time_to_fill_buffer * 5)
            self.buffer = np.concatenate((self.buffer, data), axis=0)
            retry = retry - 1
            if retry < 1:
                print("failed to fill read buffer")

    def read_filtered(self):
        self.fill_read_buffer()
        read_matrix = np.asmatrix(self.buffer[:READ_BUFFER_DEPTH, :])
        self.buffer = self.buffer[READ_BUFFER_DEPTH:, :]
        read_matrix = np.apply_along_axis(notch, 0, read_matrix)[0]
        read_matrix = np.apply_along_axis(bandpass, 0, read_matrix)
        return read_matrix


def main():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    sensor_wrapper = SensorWrapper()
    sensor_wrapper.connect()
    sleep(3)
    data = sensor_wrapper.read_filtered()
    sensor_wrapper.disconnect()

    # demo how to convert it to pandas DF and plot data
    df = pd.DataFrame(data)
    print('Data From the Board')
    print(df.head(10))


if __name__ == "__main__":
    main()
