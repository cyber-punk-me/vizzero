import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QSplitter, QWidget, QTabWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import Qt

import draw
import threading
import FileWriter
import handsim
from sensorwrapper import SensorWrapper
import subprocess

N_PASSES = 1 # number of dropped frames for 1 drawing
DRAW_BUFFER_SIZE = 25 # it's 20 fps if n_passes = 1
WRITE_BUFFER_SIZE = 100
RECORDING_DURATION = 5. # seconds


class DataThread(threading.Thread):

    data_running = True

    def __init__(self, canvas):
        super(DataThread, self).__init__()
        self.canvas = canvas
        self.file_writer = FileWriter.FileWriter()
        self.sensor = None

    def stop(self):
        self.data_running = False

    def run(self):
        nb_chan = 8
        verbose = True
        # Create a new python interface.
        self.sensor = SensorWrapper()
        self.sensor.connect()
        try:
            while self.data_running:
                data = self.sensor.read_filtered()
                self.canvas.feed_data(data, data.shape[0])
        except BaseException as e:
            print(e.with_traceback())
        finally:
            self.sensor.disconnect()


class Tabs(QTabWidget):
    def __init__(self):
        super(Tabs, self).__init__()
        self.all_tabs = []
        self.handsim_view = handsim.create_hand_sim_widget()
        self.build_widgets()

    def build_widgets(self):
        self.all_tabs.append(self.handsim_view)
        self.addTab(self.all_tabs[0], 'Sim')
        self.all_tabs.append(QWidget())
        self.addTab(self.all_tabs[1], 'Fixed')
        self.all_tabs.append(QWidget())
        self.addTab(self.all_tabs[2], 'Keyboard')
        self.all_tabs.append(QWidget())
        self.addTab(self.all_tabs[3], 'Сontinuous')


#    def create_tab(self):
#        self.all_tabs.append(QtWidgets.QWidget())
#        self.addTab(self.all_tabs[len(self.all_tabs) - 1],
#                    'Tab {}'.format(len(self.all_tabs)))

    def close_tab(self, index):
        widget = self.widget(index)
        widget.deleteLater()
        self.removeTab(index)


class MainWindow(QMainWindow):

    data_thread = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('vizzero')

        vbox = QVBoxLayout(self)
        window = QWidget()
        window.setLayout(vbox)

        self.myo_canvas = draw.Canvas()
        self.myo_canvas.native.setParent(window)

        self.btnStart = QPushButton("Start data")
        self.btnStop = QPushButton("Stop data")
        vbox.addWidget(self.btnStart)
        vbox.addWidget(self.btnStop)
        vbox.addWidget(self.myo_canvas.native)

        self.btnStart.clicked.connect(self.on_start)
        self.btnStop.clicked.connect(self.on_stop)
        self.node_proc = None

        self.tabs = Tabs()
        self.handsim_view = self.tabs.handsim_view
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.tabs)
        splitter1.addWidget(window)
        splitter1.setSizes([70, 30])

        self.setCentralWidget(splitter1)

    def on_start(self):
        if self.data_thread is None:
            self.data_thread = DataThread(self.myo_canvas)
            self.data_thread.start()

    def on_stop(self):
        if self.data_thread is not None:
            self.data_thread.stop()
            self.data_thread.join()
            self.data_thread = None

def main(argv):
    appQt = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Starting and stopping the process")
    window.show()
    ret = appQt.exec_()
    print("quitting")
    window.on_stop()
    sys.exit(ret)


if __name__ == '__main__':
    main(sys.argv[1:])
