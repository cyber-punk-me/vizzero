from PySide2.QtWidgets import QSplitter, QFrame, QPushButton, QGroupBox, QGridLayout, QFileDialog, \
    QHBoxLayout, QLabel
from PySide2.QtCore import Qt, QSize, QTimer
from PySide2.QtGui import QIcon
from enum import Enum

import sys
sys.path.append('../../../')

# import module from parent directory
import core.core

WAIT_BEFORE_RECORDING = 5  # seconds
RECORDING_DURATION = 5  # seconds


class Gestures(Enum):
    nothing = 0
    rock = 1
    scissors = 2
    paper = 3
    ok = 4
    horns = 5
    shaka = 6
    gun = 7
    thumbs_up = 8


class RecordHandFixed(core.core.BasePlugin):
    def __init__(self, core_controller):
        super().__init__(core_controller)
        self.core_controller = core_controller
        self.current_path = None
        self.path_label = QLabel()
        self.path_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.tips_label = QLabel('Select directory to start recording process')
        self.timer_before_recording = None
        self.waited_sec = 0
        self.data_thread = None
        self.gesture_buttons = dict()
        self.not_recorded_gestures = list(Gestures)

    def on_dir_selection(self):
        dir = QFileDialog.getExistingDirectory()
        if dir == '':
            return
        self.current_path = dir
        self.path_label.setText(self.current_path)
        self.not_recorded_gestures = list(Gestures)
        for button in self.gesture_buttons.values():
            button.setEnabled(True)
        self.tips_label.setText('Select gesture')

    def stop_recording(self):
        self.core_controller.finish_file()
        for not_recorded_gesture in self.not_recorded_gestures:
            self.gesture_buttons[not_recorded_gesture].setEnabled(True)
        if len(self.not_recorded_gestures) == 0:
            self.tips_label.setText('All gestures are recorded, select the new folder to record another dataset')
        else:
            self.tips_label.setText('File is saved, select the next gesture')

    def recording(self, gesture):
        self.core_controller.write_to_file(self.current_path, gesture)
        self.tips_label.setText('Recording...')
        QTimer.singleShot(RECORDING_DURATION * 1000, self.stop_recording)

    def show_timer(self, gesture):
        self.tips_label.setText('Wait {} sec'.format(WAIT_BEFORE_RECORDING - self.waited_sec))
        if (self.waited_sec == WAIT_BEFORE_RECORDING):
            self.waited_sec = 0
            self.timer_before_recording.stop()
            self.recording(gesture)
            return
        self.waited_sec += 1

    def on_gesture_selection(self, gesture):
        if self.core_controller.sensor_controller.sensor_connected():
            self.gesture_buttons[gesture].setEnabled(False)
            self.not_recorded_gestures.remove(gesture)
            for not_recorded_gesture in self.not_recorded_gestures:
                self.gesture_buttons[not_recorded_gesture].setEnabled(False)
            self.timer_before_recording = QTimer()
            self.timer_before_recording.timeout.connect(lambda: self.show_timer(gesture))
            self.timer_before_recording.start(1000)

    def create_gestures_group_box(self):
        gestures_group_box = QGroupBox()
        gridLayout = QGridLayout()

        icon_size = QSize(150, 100)
        path_to_images = '../gestures/photos/'

        button_nothing = QPushButton()
        button_nothing.clicked.connect(lambda: self.on_gesture_selection(Gestures.nothing))
        button_nothing.setIcon(QIcon(path_to_images + 'nothing.jpg'))
        gridLayout.addWidget(button_nothing, 0, 0)
        self.gesture_buttons[Gestures.nothing] = button_nothing

        button_rock = QPushButton()
        button_rock.clicked.connect(lambda: self.on_gesture_selection(Gestures.rock))
        button_rock.setIcon(QIcon(path_to_images + 'rock.jpg'))
        gridLayout.addWidget(button_rock, 0, 1)
        self.gesture_buttons[Gestures.rock] = button_rock

        button_scissors = QPushButton()
        button_scissors.clicked.connect(lambda: self.on_gesture_selection(Gestures.scissors))
        button_scissors.setIcon(QIcon(path_to_images + 'scissors.jpg'))
        gridLayout.addWidget(button_scissors, 0, 2)
        self.gesture_buttons[Gestures.scissors] = button_scissors

        button_paper = QPushButton()
        button_paper.clicked.connect(lambda: self.on_gesture_selection(Gestures.paper))
        button_paper.setIcon(QIcon(path_to_images + 'paper.jpg'))
        gridLayout.addWidget(button_paper, 1, 0)
        self.gesture_buttons[Gestures.paper] = button_paper

        button_ok = QPushButton()
        button_ok.clicked.connect(lambda: self.on_gesture_selection(Gestures.ok))
        button_ok.setIcon(QIcon(path_to_images + 'ok.jpg'))
        gridLayout.addWidget(button_ok, 1, 1)
        self.gesture_buttons[Gestures.ok] = button_ok

        button_horns = QPushButton()
        button_horns.clicked.connect(lambda: self.on_gesture_selection(Gestures.horns))
        button_horns.setIcon(QIcon(path_to_images + 'horns.jpg'))
        gridLayout.addWidget(button_horns, 1, 2)
        self.gesture_buttons[Gestures.horns] = button_horns

        button_shaka = QPushButton()
        button_shaka.clicked.connect(lambda: self.on_gesture_selection(Gestures.shaka))
        button_shaka.setIcon(QIcon(path_to_images + 'shaka.jpg'))
        gridLayout.addWidget(button_shaka, 2, 0)
        self.gesture_buttons[Gestures.shaka] = button_shaka

        button_gun = QPushButton()
        button_gun.clicked.connect(lambda: self.on_gesture_selection(Gestures.gun))
        button_gun.setIcon(QIcon(path_to_images + 'gun.jpg'))
        gridLayout.addWidget(button_gun, 2, 1)
        self.gesture_buttons[Gestures.gun] = button_gun

        button_thumb = QPushButton()
        button_thumb.clicked.connect(lambda: self.on_gesture_selection(Gestures.thumbs_up))
        button_thumb.setIcon(QIcon(path_to_images + 'thumbs_up.jpg'))
        gridLayout.addWidget(button_thumb, 2, 2)
        self.gesture_buttons[Gestures.thumbs_up] = button_thumb

        for button in self.gesture_buttons.values():
            button.setEnabled(False)
            button.setIconSize(icon_size)

        gestures_group_box.setLayout(gridLayout)
        return gestures_group_box

    def create_widget(self, parent=None):
        main_group_box = QGroupBox()
        main_layout = QHBoxLayout()

        top = QFrame()
        top_layout = QGridLayout()
        top_layout.setColumnStretch(0, 2)
        top_layout.setColumnStretch(1, 1)

        top_layout.addWidget(self.tips_label, 0, 0)
        top_layout.addWidget(self.path_label, 1, 0)

        self.button_folder_selection = QPushButton('Select directory')
        self.button_folder_selection.clicked.connect(lambda: self.on_dir_selection())
        top_layout.addWidget(self.button_folder_selection, 1, 1)

        top.setLayout(top_layout)
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(top)

        gestures_group_box = self.create_gestures_group_box()
        splitter.addWidget(gestures_group_box)

        splitter.setSizes([50, 200])
        main_layout.addWidget(splitter)
        main_group_box.setLayout(main_layout)

        return main_group_box

    def destroy(self):
        self.core_controller.finish_file()

    def get_name(self):
        return "Fixed"
