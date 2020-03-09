from PySide2.QtWidgets import QMainWindow, QApplication, QSplitter, QWidget, QTabWidget, QVBoxLayout
from PySide2.QtCore import Qt

from core.core import *
from plugins.handsim.plugin import Handsim
from plugins.record_hand_fixed.plugin import RecordHandFixed
from widgets.realtime import RealtimeCanvas
from rx.scheduler import ThreadPoolScheduler


class Tabs(QTabWidget):
    def __init__(self, core_controller, plugins):
        super(Tabs, self).__init__()
        self.core_controller = core_controller
        self.plugins = plugins
        self.build_widgets()

    def build_widgets(self):
        for plugin in self.plugins:
            self.addTab(plugin.create_widget(), plugin.get_name())

    def close_tab(self, index):
        widget = self.widget(index)
        widget.deleteLater()
        self.removeTab(index)


class MainWindow(QMainWindow):

    core_controller = None
    plugins = None
    draw_data_scheduler = ThreadPoolScheduler(1)

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('vizzero')

        self.core_controller = CoreController()
        self.plugins = [Handsim(self.core_controller), RecordHandFixed(self.core_controller)]

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

        self.btnStart.clicked.connect(self.start_data)
        self.btnStop.clicked.connect(self.stop_data)
        self.node_proc = None

        self.tabs = Tabs(self.core_controller, self.plugins)
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.tabs)
        splitter1.addWidget(window)
        splitter1.setSizes([70, 30])

        self.setCentralWidget(splitter1)

        self.core_controller.sensor_controller.rx_sensor_data_subject\
            .subscribe(self.myo_canvas.feed_data, scheduler=self.draw_data_scheduler)

    def start_data(self):
        self.core_controller.start_data()

    def stop_data(self):
        self.core_controller.stop_data()

    def closeEvent(self, event):
        for plugin in self.plugins:
            try:
                plugin.destroy()
            finally:
                pass


def main(argv):
    appQt = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Starting and stopping the process")
    window.show()
    ret = appQt.exec_()
    print("quitting")
    window.stop_data()
    sys.exit(ret)


if __name__ == '__main__':
    main(sys.argv[1:])
