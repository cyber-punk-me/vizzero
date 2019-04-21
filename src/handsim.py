import threading
from time import sleep

from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
from WSServer import *

sys.path.append('./handsim')


def create_hand_sim_widget(parent=None):
    create_in_new_thread()
    view = QWebEngineView(parent)
    view.setUrl(QUrl.fromLocalFile(QDir.currentPath() + "/../handjs/index.html"))
    return view

