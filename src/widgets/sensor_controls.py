from PySide2.QtWidgets import QGridLayout, QPushButton, QLabel, QCheckBox, QGroupBox, QLineEdit

from core.core import CoreController


class SensorControls(QGroupBox):

    def __init__(self, core_controller: CoreController):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.setMaximumHeight(400)
        # simulate
        simulate_group = QGroupBox()
        simulate_layout = QGridLayout()
        simulate_group.setLayout(simulate_layout)
        simulate_label = QLabel('Simulate')
        simulate_checkbox = QCheckBox()

        simulate_layout.addWidget(simulate_label, 0, 0)
        simulate_layout.addWidget(simulate_checkbox, 0, 1)
        layout.addWidget(simulate_group, 0, 0, 1, 2)

        # bandpass
        bandpass_group = QGroupBox()
        bandpass_layout = QGridLayout()
        bandpass_group.setLayout(bandpass_layout)
        bandpass_label = QLabel('Bandpass')
        bandpass_checkbox = QCheckBox()

        bp_high_label = QLabel('High, Hz')
        bp_high_input = QLineEdit()
        bp_low_label = QLabel('Low, Hz')
        bp_low_input = QLineEdit()

        bandpass_layout.addWidget(bandpass_label, 0, 0)
        bandpass_layout.addWidget(bandpass_checkbox, 0, 1)
        bandpass_layout.addWidget(bp_high_label, 1, 0)
        bandpass_layout.addWidget(bp_high_input, 1, 1)
        bandpass_layout.addWidget(bp_low_label, 2, 0)
        bandpass_layout.addWidget(bp_low_input, 2, 1)
        layout.addWidget(bandpass_group, 1, 0, 1, 2)

        # notch
        notch_group = QGroupBox()
        notch_layout = QGridLayout()
        notch_group.setLayout(notch_layout)
        notch_label = QLabel('Notch')
        notch_checkbox = QCheckBox()

        notch_input_label = QLabel('Notch, Hz')
        notch_input = QLineEdit()
        notch_layout.addWidget(notch_label, 0, 0)
        notch_layout.addWidget(notch_checkbox, 0, 1)
        notch_layout.addWidget(notch_input_label, 1, 0)
        notch_layout.addWidget(notch_input, 1, 1)
        layout.addWidget(notch_group, 2, 0, 1, 2)

        # start/stop
        btn_start = QPushButton("Start data")
        btn_stop = QPushButton("Stop data")
        btn_start.clicked.connect(core_controller.start_data)
        btn_stop.clicked.connect(core_controller.stop_data)
        layout.addWidget(btn_start, 3, 0)
        layout.addWidget(btn_stop, 3, 1)
