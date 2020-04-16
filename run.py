from tkinter import *
import time
import datetime
import os
import glob


ARTS_RES_PATH = 'arts_res'

def mk_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def load_arts_res(path):
    print('[INFO] check folder')
    mk_dir(path)
    print('[INFO] check arts resources')
    for i in glob.glob(path+'/*'):
        print(i)


if __name__ == "__main__":
    # run()
    load_arts_res(ARTS_RES_PATH)
    pass