#!/usr/bin/python3

import sys
import cv2
import argparse
import numpy as np
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("url", help="MJPEG URL of the source to read from")
parser.add_argument("out", help="Destination file to save")
parser.add_argument("--flip", help="Flip the image")
args = parser.parse_args()

if not args.url:
    print("url is required")
    sys.exit(1)

out = cv2.VideoWriter(
    args.out,
    cv2.VideoWriter_fourcc(*'XVID'),
    30.0,
    (640, 480))

with urllib.request.urlopen(args.url) as stream:
    bytes = b''
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            try:
                if not len(jpg):
                    continue
                frame = cv2.imdecode(
                    np.fromstring(jpg, dtype=np.uint8),
                    cv2.IMREAD_COLOR)
            except ValueError as e:
                print(e)
                continue
            if args.flip:
                frame = cv2.flip(frame, 0)
            out.write(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(10) == 27:
                break

out.release()
cv2.destroyAllWindows()
