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

            try:
                resp = server.handleRequest(req) 
            except Exception as e:
                # don't propogate exception; handler is responsible for being exception safe, and we have no reason to close the connection
                logger.exception(e)
                resp = HttpResponse(500)
            
            logger.info(f"Writing response {str(resp)}")
            resp.writeResponse(buffered_conn)
        logger.info(f"Connection with {addr} terminated normally")
    except socket.timeout:
        logger.info(f"Connection timed out with {addr}")
    except Exception as e:
        # Exception must have been during server code; log and terminate this worker
        logger.exception(e)
    finally:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
