from PySide2.QtGui import QDoubleValidator
from PySide2.QtWidgets import QGridLayout, QPushButton, QLabel, QCheckBox, QGroupBox, QLineEdit, QComboBox

from core.core import SensorController
from sensor.sensor_wrapper import SensorSettings


class SensorControls(QGroupBox):

    sensor_controller: SensorController = None
    simulate_checkbox: QCheckBox = None
    sensor_port_input: QComboBox = None
    amplitude_scale_input: QLineEdit = None

    def update_sensor_settings(self, simulate=None, com_port=None, amplitude_scale=None):
        sensor_settings: SensorSettings = self.sensor_controller.get_sensor_settings()
        if simulate is not None:
            sensor_settings.simulation = simulate
        if com_port is not None:
            sensor_settings.sensor_com_port = com_port
        if amplitude_scale is not None:
            sensor_settings.amplitude_scale = amplitude_scale
        self.sensor_controller.update_sensor_settings(sensor_settings)

    def simulate_clicked(self, checked):
        self.update_sensor_settings(simulate=checked)

    def com_port_changed(self, com_port):
        self.update_sensor_settings(com_port=com_port)

    def amplitude_scale_changed(self, amplitude_scale):
        try:
            self.update_sensor_settings(amplitude_scale=float(amplitude_scale))
        except:
            None

    def update_com_items(self):
        com_ports = self.sensor_controller.list_serial_ports()
        while self.sensor_port_input.count() > 0:
            self.sensor_port_input.removeItem(0)
        for com_port in com_ports:
            self.sensor_port_input.addItem(com_port)

    def bind_controls(self):
        self.update_com_items()
        self.simulate_checkbox.stateChanged.connect(self.simulate_clicked)
        self.sensor_port_input.currentIndexChanged.connect(self.com_port_changed)
        self.sensor_port_input.activated.connect(self.update_com_items)
        self.amplitude_scale_input.textEdited.connect(self.amplitude_scale_changed)

    def draw_sensor_settings(self, sensor_settings: SensorSettings):
        self.simulate_checkbox.setChecked(sensor_settings.simulation)
        amplitude_text_position = self.amplitude_scale_input.cursorPosition()
        self.amplitude_scale_input.setText(sensor_settings.amplitude_scale.__str__())
        self.amplitude_scale_input.setCursorPosition(min(amplitude_text_position, self.amplitude_scale_input.cursorPosition()))

    def __init__(self, sensor_controller: SensorController):
        super().__init__()
        self.sensor_controller = sensor_controller
        layout = QGridLayout()
        self.setLayout(layout)
        self.setMaximumHeight(400)
        # simulate
        select_sensor_group = QGroupBox()
        simulate_layout = QGridLayout()
        select_sensor_group.setLayout(simulate_layout)
        simulate_label = QLabel('Simulate')
        self.simulate_checkbox = QCheckBox()
        sensor_port_label = QLabel('Sensor COM')
        self.sensor_port_input = QComboBox()
        self.sensor_port_input.setEditable(True)
        amplitude_scale_label = QLabel('Scale')
        self.amplitude_scale_input = QLineEdit()
        self.amplitude_scale_input.setValidator(QDoubleValidator(0.0, 1.0, 10))

        simulate_layout.addWidget(simulate_label, 0, 0)
        simulate_layout.addWidget(self.simulate_checkbox, 0, 1)
        simulate_layout.addWidget(sensor_port_label, 1, 0)
        simulate_layout.addWidget(self.sensor_port_input, 1, 1)
        simulate_layout.addWidget(amplitude_scale_label, 2, 0)
        simulate_layout.addWidget(self.amplitude_scale_input, 2, 1)
        layout.addWidget(select_sensor_group, 0, 0, 1, 2)

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
        btn_start.clicked.connect(sensor_controller.start_data)
        btn_stop.clicked.connect(sensor_controller.stop_data)
        layout.addWidget(btn_start, 3, 0)
        layout.addWidget(btn_stop, 3, 1)

        self.bind_controls()
        self.sensor_controller.rx_sensor_settings_subject.subscribe(self.draw_sensor_settings)
