import cv2
import numpy as np
import urllib.request


class MjpegDecoder:
    def __init__(self, url, bytes_step=512):
        self.url = url
        self.boundary = None
        self.stream = None
        self.bytes_step = bytes_step

    def open(self):
        if not self.stream:
            self.stream = urllib.request.urlopen(self.url)
            self.boundary = b'--' + bytearray(
                self.stream.info()['content-type'].split('=')[1], 'utf-8')

    def read(self):
        self.open()
        next = False
        bytes = b''
        while True:
            bytes += self.stream.read(self.bytes_step)
            # seek boundary
            bb = bytes.find(self.boundary)
            if bb == -1:
                continue

            jpg = []
            if not next:
                # remove frame headers (like content type, length, etc)
                # headers end with a double carriage return
                a = bytes.find(b'\r\n\r\n', bb)
                bytes = bytes[a+4:]
                next = True
                continue
            else:
                jpg = bytes[:bb]
                bytes[:bb]
                next = False

            if len(jpg):
                frame = cv2.imdecode(
                    np.fromstring(jpg, dtype=np.uint8),
                    cv2.IMREAD_COLOR)

                if frame is not None and len(frame):
                    return frame
