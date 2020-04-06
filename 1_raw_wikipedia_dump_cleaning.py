import os
import datetime

def clean(src, dest=None):
    buff_size = 100000
    i = 0
    prev = 0
    res = ''
    while True:
        prev = src.tell()
        char = ''
        try:
            char = src.read(1)
        except:
            continue
        if prev == src.tell():
            break
        try:
            res += char
            if len(res) == buff_size and dest is not None:
                dest.write(res)
                res = ''
        except:
            continue
        if char == '\n':
            i += 1
        print('\rines processed: {}\r'.format(i), end='\r', flush=True)
    return res

src = input('input file name: ')
dest = input('output file name: ')
clean(src, dest)
print('script finished at', datetime.datetime.now())
