#!/usr/bin/python3

import sys
import time
import cv2
import argparse
import mjpeg

parser = argparse.ArgumentParser()
parser.add_argument("url", help="MJPEG URL of the source to read from")
parser.add_argument("--flip", help="Flip the image")
args = parser.parse_args()

if not args.url:
    print("url is required")
    sys.exit(1)


def main():

    cap = mjpeg.MjpegDecoderAsync(args.url)
    cap.open()
    while cap.isOpened():

        ok, frame = cap.read()
        if frame is None:
            break

        if args.flip:
            frame = cv2.flip(frame, 0)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord("q"):
            cap.release()
            break
    cv2.destroyAllWindows()


main()
