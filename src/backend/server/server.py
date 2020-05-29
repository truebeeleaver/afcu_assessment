import socket
import logging
import threading

from backend.server.request import HttpRequest
from backend.server.response import HttpResponse
from backend.server.connection import handleConnection

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
                    target=handleConnection, args=(self, conn, addr)
                )
                thread.start()

                (conn, addr) = sock.accept()
        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

    # VERY basic resource handling. I am not accounting for query args or path resolution (ie /api/profile/../profile == /api/profile)
    # Obviously this is necessary for a robust server but I don't want to get too into the weeds
    def bindResource(self, resource, handler, args):
        self.handlers[resource] = (handler, args)

    def handleRequest(self, req):
        if req.resource in self.handlers:
            (handler, args) = self.handlers[req.resource]
            return handler(req, args)
        return HttpResponse(404)
