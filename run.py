from tkinter import *
import os
import glob
import time
import datetime
from estimate_keypoints import SKP


ARTS_RES_PATH = 'arts_res'
ARTS_SKP_PATH = 'skp_output'

def mk_dir(path):
    if os.path.isdir(path):
        return True
    else:
        print('[INFO] make folder')
        return True if os.mkdir(path) else False


def get_file_basename(path):
    basename = os.path.splitext(os.path.basename(path))[0]
    return basename


def load_arts_res():
    arts_res = set()
    skp_res = set()
    

    print('[INFO] check folder')

    if mk_dir(ARTS_RES_PATH):
        arts_res = set(map(get_file_basename, glob.glob(ARTS_RES_PATH + '/*')))
        print('[INFO] check arts resources: {} files'.format(len(arts_res)))

    if mk_dir(ARTS_SKP_PATH):
        skp_res = set(map(get_file_basename, glob.glob(ARTS_SKP_PATH + '/*')))
        print('[INFO] check skp resources: {} files'.format(len(skp_res)))

    diff = arts_res.difference(skp_res)
    if diff:
        skp = SKP()
        for i in diff:
            skp.get_skp_from_pic(os.path.join(ARTS_RES_PATH, i+".jpg"))


if __name__ == "__main__":
    # run()
    load_arts_res()
