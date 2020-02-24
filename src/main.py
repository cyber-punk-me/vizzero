import sys
import traceback
from PySide2.QtWidgets import QMainWindow, QApplication, QSplitter, QWidget, QTabWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import QUrl, QDir
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import Qt

import threading
from core import *
from handsim.handsim import *
from file.fileUtil import *
from widgets.realtime import RealtimeCanvas
from widgets.recordHandFixed import RecordHandFixed


def create_hand_sim_widget(parent=None):
    view = QWebEngineView(parent)
    view.setUrl(QUrl.fromLocalFile(QDir.currentPath() + "/../handjs/index.html"))
    return view


class Tabs(QTabWidget):
    def __init__(self, core_controller):
        super(Tabs, self).__init__()
        self.core_controller = core_controller
        self.all_tabs = []
        self.handsim_view = create_hand_sim_widget()
        self.build_widgets()

    def build_widgets(self):
        self.all_tabs.append(self.handsim_view)
        self.addTab(self.all_tabs[0], 'Sim')
        self.all_tabs.append(RecordHandFixed(self.core_controller).create_recording_fixed_widget())
        self.addTab(self.all_tabs[1], 'Fixed')
        self.all_tabs.append(QWidget())
        self.addTab(self.all_tabs[2], 'Keyboard')
        self.all_tabs.append(QWidget())
        self.addTab(self.all_tabs[3], 'Сontinuous')
#
#    def create_tab(self):
#        self.all_tabs.append(QtWidgets.QWidget())
#        self.addTab(self.all_tabs[len(self.all_tabs) - 1],
#                    'Tab {}'.format(len(self.all_tabs)))

    def close_tab(self, index):
        widget = self.widget(index)
        widget.deleteLater()
        self.removeTab(index)


class MainWindow(QMainWindow):

    core_controller = None
    handsim_server = None

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('vizzero')

        vbox = QVBoxLayout(self)
        window = QWidget()
        window.setLayout(vbox)

        self.myo_canvas = RealtimeCanvas()
        self.myo_canvas.native.setParent(window)

        self.btnStart = QPushButton("Start data")
        self.btnStop = QPushButton("Stop data")
        vbox.addWidget(self.btnStart)
        vbox.addWidget(self.btnStop)
        vbox.addWidget(self.myo_canvas.native)

        self.btnStart.clicked.connect(self.on_start)
        self.btnStop.clicked.connect(self.on_stop)
        self.node_proc = None

        self.handsim_server = HandsimThread()
        self.handsim_server.start()

        self.core_controller = CoreController()
        self.tabs = Tabs(self.core_controller)
        self.handsim_view = self.tabs.handsim_view
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.tabs)
        splitter1.addWidget(window)
        splitter1.setSizes([70, 30])

        self.setCentralWidget(splitter1)

        self.core_controller.sensor_controller.rx_sensor_data_subject.subscribe(self.myo_canvas.feed_data)

    def on_start(self):
        self.core_controller.sensor_controller.start_data()

    def on_stop(self):
        self.core_controller.sensor_controller.stop_data()


def main(argv):
    appQt = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Starting and stopping the process")
    window.show()
    ret = appQt.exec_()
    print("quitting")
    window.on_stop()
    window.handsim_server.stop()
    sys.exit(ret)


if __name__ == '__main__':
    main(sys.argv[1:])
