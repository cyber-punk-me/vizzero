import datetime
import os
import glob
import numpy as np

class FileWriter:
    def __init__(self, path_to_file="data/"):
        self._path = path_to_file if path_to_file.endswith('/') else (path_to_file + "/")
        self.f = None

    def start_file(self):
        filename = str(datetime.datetime.today().strftime("%Y-%m-%d_%H_%M_%S")) + ".csv"
        path_file = self._path + filename
        self.f = open(path_file, 'a')

    def append_data(self, data):
        np.savetxt(self.f, data, delimiter=',')

    def finish_file(self):
        self.f.close()

    def delete_latest_file(self):
        files = sorted(glob.glob(self._path + "*.csv"))
        if len(files) != 0:
            os.remove(files[-1])