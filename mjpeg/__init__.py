import cv2
import numpy as np
import urllib.request
import threading
import queue


def _read(queue, closed, url, bytes_step):
    cap = MjpegDecoder(url, bytes_step)
    while cap.isOpened() and not closed.is_set():
        ok, frame = cap.read()
        if ok:
            try:
                queue.put(frame, block=False)
            except queue.Full:
                pass

    cap.release()


class MjpegDecoderAsync:
    def __init__(self, url, bytes_step=None, max_frames=0):
        self.url = url
        self.bytes_step = bytes_step
        self.max_frames = max_frames
        self.queue = queue.Queue(max_frames)
        self.closed = threading.Event()
        self.thread = None
        self.cache_thread = None
        self.open()

    def isOpened(self):
        return self.thread is not None

    def open(self):
        if not self.isOpened():
            self.thread = threading.Thread(
                target=_read,
                args=(
                    self.queue,
                    self.closed,
                    self.url,
                    self.bytes_step
                )
            )
            self.thread.start()

    def read(self):
        try:
            frame = self.queue.get(block=False)
            return True, frame
        except queue.Empty:
            pass
        return False, None

    def release(self):
        self.closed.set()
        self.thread.join()
        self.thread = None


class MjpegDecoder:
    def __init__(self, url, bytes_step=None):
        self.url = url
        self.boundary = None
        self.stream = None
        self.bytes_step = bytes_step if bytes_step is not None else 1024
        self.open()

    def isOpened(self):
        return self.stream is not None

    def open(self):
        if not self.isOpened():
            self.stream = urllib.request.urlopen(self.url)
            self.boundaries = [
                b'\r\n--' + bytearray(
                    self.stream.info()['content-type'].split('=')[1], 'utf-8'
                ),
                b"\r\n\r\n"
            ]

    def release(self):
        self.stream.close()
        self.stream = None

    def read(self):

        next = False
        bytes = b''
        start_boundary, end_boundary = self.boundaries

        while True:

            bytes += self.stream.read(self.bytes_step)

            # seek boundary
            end_image = bytes.find(end_boundary)
            if end_image == -1:
                continue

            jpg = None
            if not next:
                # remove frame headers (like content type, length, etc)
                # headers end with a double carriage return
                start_image = bytes.find(end_boundary, end_image)
                bytes = bytes[start_image+len(end_boundary):]
                next = True
                continue
            else:
                jpg = bytes[:end_image]
                bytes[:end_image]
                next = False

            if jpg is not None:
                frame = cv2.imdecode(
                    np.fromstring(jpg, dtype=np.uint8),
                    cv2.IMREAD_COLOR)

                if frame is not None and len(frame):
                    return [True, frame]
