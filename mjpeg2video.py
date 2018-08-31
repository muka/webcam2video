#!/usr/bin/python3

import sys
import cv2
import argparse
import mjpeg

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
    (1920, 1080))


def main():
    decoder = mjpeg.MjpegDecoder(args.url)
    while True:
        frame = decoder.read()
        if args.flip:
            frame = cv2.flip(frame, 0)
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(10) == 27:
            break
    out.release()
    cv2.destroyAllWindows()


main()
