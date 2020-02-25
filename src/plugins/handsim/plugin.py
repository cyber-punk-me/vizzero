import sys
import threading

from PySide2.QtCore import QUrl, QDir
from PySide2.QtWebEngineWidgets import QWebEngineView

sys.path.append('../../')
from core.core import BasePlugin
from .server import *


class Handsim(BasePlugin):

    handsim_server_thread = None

    def __init__(self, core_controller):
        super().__init__(core_controller)
        self.handsim_server_thread = HandsimThread()
        self.handsim_server_thread.start()

    def create_widget(self, parent=None):
        view = QWebEngineView(parent)
        view.setUrl(QUrl.fromLocalFile(QDir.currentPath() + "/../handjs/index.html"))
        return view

    def destroy(self):
        self.handsim_server_thread.stop()

    def get_name(self):
        return "Handsim"


class HandsimThread(threading.Thread):

    def __init__(self):
        super(HandsimThread, self).__init__()
        self.running = False
        self.handsim_server = None

    def run(self):
        self.running = True
        self.handsim_server = HandSimServer()
        self.handsim_server.start()

    def stop(self):
        self.running = False
        if self.handsim_server is not None:
            self.handsim_server.stop()
        self.join()


