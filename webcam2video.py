#!/usr/bin/python3

import numpy as np
import cv2
import argparse

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL of the source to read from")
parser.add_argument("out", help="Destination file to save")
args = parser.parse_args()

url = args.url
if is_number(url):
    print("Using camera %s" % (url))
    url = int(url)

source = cv2.VideoCapture(url)
out = cv2.VideoWriter(args.out, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640,480))

while(source.isOpened()):
    ret, frame = source.read()
    if ret==True:
        frame = cv2.flip(frame,0)
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(10) == 27:
            break
    else:
        println("Read failed")
        break

source.release()
out.release()

cv2.destroyAllWindows()
