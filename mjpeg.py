import cv2
import numpy as np
import urllib.request
from collections import deque


class MjpegDecoder:
    def __init__(self, url, cache_length=30):
        self.cache_length = cache_length
        self.url = url
        self.cache = deque([], maxlen=cache_length)

    def read(self):
        if not len(self.cache):
            return None
        return self.cache.popleft()

    def clear(self):
        return self.cache.clear()

    async def open(self):
        with urllib.request.urlopen(self.url) as stream:
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
                        self.cache.append(frame)
                    except ValueError as e:
                        print(e)
                        continue
