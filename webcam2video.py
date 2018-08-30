#!/usr/bin/python3

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
parser.add_argument("flip", help="Flip the image")
args = parser.parse_args()

url = args.url
if is_number(url):
    print("Using camera %s" % (url))
    url = int(url)

source = cv2.VideoCapture(url)
out = cv2.VideoWriter(
    args.out,
    cv2.VideoWriter_fourcc(*'XVID'),
    30.0,
    (640, 480))

while(source.isOpened()):
    ret, frame = source.read()
    if ret is True:
        if args.flip:
            frame = cv2.flip(frame, 0)
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(10) == 27:
            break
    else:
        print("Read error")

source.release()
out.release()

cv2.destroyAllWindows()
