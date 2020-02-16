import sys
import threading
sys.path.append('./handsim')
from handSimServer import HandSimServer


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


