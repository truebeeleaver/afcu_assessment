import socket
import logging
import threading

from .connection import handleConnection

logger = logging.getLogger(__name__)


class Server:
    def __init__(self):
        pass

    # Listen until a shutdown signal is passed
    def run(self):
        # TODO lift hardcoded stuff out into at least main module
        self.ip_addr = "127.0.0.1"
        self.port = 8080

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
