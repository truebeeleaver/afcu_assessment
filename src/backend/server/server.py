import socket
import logging
import threading

from .connection import handleConnection

logger = logging.getLogger(__name__)


class Server:
    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port
        self.handlers = {}

    # Listen until a shutdown signal is passed
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.ip_addr, self.port))
        sock.listen()

        logger.info(f"Listening on {self.ip_addr}:{self.port}")

        try:
            (conn, addr) = sock.accept()
            while conn:
                logger.info(f"Connection accepted from {addr}")

                thread = threading.Thread(
                    target=handleConnection, args=(conn, addr)
                )
                thread.start()

                (conn, addr) = sock.accept()
        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()