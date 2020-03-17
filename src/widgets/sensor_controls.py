from PySide2.QtWidgets import QVBoxLayout, QPushButton

from core.core import CoreController


class SensorControls(QVBoxLayout):

    def __init__(self, core_controller: CoreController):
        super().__init__()
        self.btnStart = QPushButton("Start data")
        self.btnStop = QPushButton("Stop data")
        self.addWidget(self.btnStart)
        self.addWidget(self.btnStop)
        self.btnStart.clicked.connect(core_controller.start_data)
        self.btnStop.clicked.connect(core_controller.stop_data)
