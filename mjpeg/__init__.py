import cv2
import numpy as np
import urllib.request
import threading
import queue


def _clear_cache(asyncDecoder):
    while not asyncDecoder.closed:
        while asyncDecoder.queue.qsize() > asyncDecoder.max_frames:
            asyncDecoder.queue.get()


def _read(asyncDecoder):

    decoder = MjpegDecoder(asyncDecoder.url, asyncDecoder.bytes_step)

    while not asyncDecoder.closed:
        asyncDecoder.queue.put(decoder.read())

    decoder.close()


class MjpegDecoderAsync:
    def __init__(self, url, bytes_step=512, max_frames=0):
        self.url = url
        self.bytes_step = bytes_step
        self.max_frames = max_frames
        self.queue = queue.Queue()
        self.closed = False
        self.thread = None
        self.cache_thread = None

    def isOpened(self):
        return self.thread is not None

    def open(self):
        if not self.isOpened:
            self.thread = threading.Thread(
                target=_read,
                args=(self,)
            )
            self.thread.start()

            if self.max_frames > 0:
                self.cache_thread = threading.Thread(
                    target=_clear_cache,
                    args=(self,)
                )
                self.cache_thread.start()

    def read(self):
        self.open()
        return True, self.queue.get(block=True)

    def release(self):
        self.close()

    def close(self):
        self.closed = True
        self.thread.join()
        self.thread = None
        if self.cache_thread:
            self.cache_thread.join()
            self.cache_thread = None


class MjpegDecoder:
    def __init__(self, url, bytes_step=512):
        self.url = url
        self.boundary = None
        self.stream = None
        self.bytes_step = bytes_step

    def isOpened(self):
        return self.stream is not None

    def open(self):
        if not self.stream:
            self.stream = urllib.request.urlopen(self.url)
            self.boundary = b'--' + bytearray(
                self.stream.info()['content-type'].split('=')[1], 'utf-8')

    def release(self):
        self.close()

    def close(self):
        self.stream.close()
        self.stream = None

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
                    return True, frame
