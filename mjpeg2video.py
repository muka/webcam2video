#!/usr/bin/python3

import sys
import cv2
import argparse
import mjpeg
import asyncio

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


async def start():

    dec = mjpeg.MjpegDecoder(args.url)
    dec.open()

    while True:
        frame = dec.read()
        if not frame:
            continue
        if args.flip:
            frame = cv2.flip(frame, 0)
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(10) == 27:
            break
    out.release()
    cv2.destroyAllWindows()

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(start())
except KeyboardInterrupt:
    loop.stop()
    pass
