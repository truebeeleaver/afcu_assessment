import socket
import logging
import threading

from backend.server.request import HttpRequest
from backend.server.response import HttpResponse
from backend.server.connection import handleConnection

logger = logging.getLogger(__name__)

def _run(server):
    server._run()

def _doAccept(sock):
    try:
        (conn, addr) = sock.accept()
        return (conn, addr)
    except socket.timeout:
        return (None, None)

class Server:
    def __init__(self, ip_addr, port):
        self.ip_addr = ip_addr
        self.port = port
        self.handlers = {}

        self.close_event = threading.Event()

    def run(self):
        thread = threading.Thread(target=_run, args=(self,))
        thread.start()
        return thread

    # Listen until a shutdown signal is passed
    def _run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Ugly, but I can't figure out why I'm not properly releasing the socket on shutdown
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind((self.ip_addr, self.port))
        sock.settimeout(5)
        sock.listen()

        logger.info(f"Listening on {self.ip_addr}:{self.port}")

        try:
            (conn, addr) = _doAccept(sock)
            while not self.close_event.is_set():
                if conn:
                    logger.info(f"Connection accepted from {addr}")

                    thread = threading.Thread(
                        target=handleConnection, args=(self, conn, addr)
                    )
                    thread.deamon = True
                    thread.start()

                (conn, addr) = _doAccept(sock)
            logger.info("Server terminating")
        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

    def stop(self):
        logger.info("Stop requested")
        self.close_event.set()

    # VERY basic resource handling. I am not accounting for query args or path resolution (ie /api/profile/../profile == /api/profile)
    # Obviously this is necessary for a robust server but I don't want to get too into the weeds
    def bindResource(self, resource, handler, args):
        self.handlers[resource] = (handler, args)

    def handleRequest(self, req):
        if req.resource in self.handlers:
            (handler, args) = self.handlers[req.resource]
            return handler(req, args)
        return HttpResponse(404)
