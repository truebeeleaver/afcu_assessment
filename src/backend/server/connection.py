import socket
import logging

from .request import HttpRequest
from .response import HttpResponse
from .util import BufferedSocket

logger = logging.getLogger(__name__)


def handleConnection(conn, addr):
    try:
        conn.settimeout(5)
        buffered_conn = BufferedSocket(conn)

        req = HttpRequest(buffered_conn)
        logger.info(f"Received request {req.verb} on {req.resource}")

        # Show a dummy page
        resp = HttpResponse(200)
        resp.setTextContent(
            "<html><body><h1>Hello World</h1></body></html>", "text/html"
        )
        
        logger.info(f"Writing response, status {resp.status}")
        resp.writeResponse(buffered_conn)
    except socket.timeout:
        logger.info(f"Connection timed out with {addr}")
    except Exception as e:
        # swallowing exceptions is Not Good in general but worker threads terminate on any errors anyway, and we want to log instead of print to console
        logger.exception(e)
