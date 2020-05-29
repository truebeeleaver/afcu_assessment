import socket
import logging

from backend.server.request import HttpRequest
from backend.server.response import HttpResponse
from backend.server.util import BufferedSocket

logger = logging.getLogger(__name__)


def handleConnection(server, conn, addr):
    try:
        buffered_conn = BufferedSocket(conn)

        # answer requests in a loop
        while conn:
            req = HttpRequest(buffered_conn)
            logger.info(f"Received request {req.verb} on {req.resource}")

            resp = server.handleRequest(req) 
            
            logger.info(f"Writing response {str(resp)}")
            resp.writeResponse(buffered_conn)
    except socket.timeout:
        logger.info(f"Connection timed out with {addr}")
    except Exception as e:
        # swallowing exceptions is Not Good in general but worker threads should terminate on any errors anyway, and we want to log instead of print to console
        # being exception safe is up to the service code
        logger.exception(e)
        # NB: conn is likely always valid here--but doc was unclear without more digging
        if conn:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
    logger.info(f"Connection with {addr} terminated normally")
