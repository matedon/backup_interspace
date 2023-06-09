# import required module
import os
import re
from datetime import datetime
os.system('cls')
# assign dir_src
#dir_src = os.getcwd() + os.sep + 'www-zip'
#dir_dest = os.getcwd() + os.sep + 'www-zip-txt'
dir_src = os.getcwd()
dir_dest = 'm:\_rclone'
#dir_src = dir_src + os.sep + '20221117_105947'

def dir(d):
    for filename in os.listdir(d):
        f = os.path.join(d, filename)
        # checking if it is a file
        if os.path.isfile(f):
            fn = f.split(os.sep)[-1]
            subdir = d.replace(dir_src, '')
            desdir = dir_dest + subdir + os.sep
            if not os.path.exists(desdir):
                os.makedirs(desdir)
            desfile = desdir + fn + '.txt'
            print('** copy **')
            print(f)
            print(desfile)
            open(desfile, 'w')
        else:
            dir(f)

dir(dir_src)