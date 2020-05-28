import logging

logger = logging.getLogger(__name__)

BUFFER_SIZE = 1024


class BufferedSocket:
    def __init__(self, conn):
        self.conn = conn
        self.buffer = b""

    def readLine(self):
        # read until a timeout or close interrupts us
        #  or we have a complete line
        while b"\r\n" not in self.buffer:
            self.buffer += self.conn.recv(BUFFER_SIZE)

        (line, self.buffer) = self.buffer.split(b"\r\n", 1)
        # headers should be utf-8
        return str(line, "utf-8")

    def readBytes(self, num_bytes):
        # read the specified number of bytes (i.e. request body)
        # We can read exactly the number we want, but the doc suggests power-of-two buffer sizes
        while len(self.buffer) < num_bytes:
            self.buffer += self.conn.recv(BUFFER_SIZE)
        ret = self.buffer[:num_bytes]
        self.buffer = self.buffer[num_bytes + 1 :]
        return ret

    def writeLine(self, line):
        buf = bytes(line, "utf-8") + b"\r\n"
        self.conn.send(buf)

    def writeBytes(self, buf):
        self.conn.send(buf)
