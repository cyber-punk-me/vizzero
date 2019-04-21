import threading
from time import sleep

from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
from WSServer import *

sys.path.append('./handsim')


#vispy canvas blocks refreshes, so forcing them here
def refresher(view):
    while True:
        time.sleep(0.05)
        t = threading.Thread(target=view.update)
        t.start()


def create_hand_sim_widget(parent=None):
    create_in_new_thread()
    view = QWebEngineView(parent)
    view.setUrl(QUrl.fromLocalFile(QDir.currentPath() + "/../handjs/index.html"))
    #refresher(view)
    return view

