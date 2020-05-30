import logging

import backend.server.request as request
from backend.server.response import HttpResponse

logger = logging.getLogger(__name__)

def handleFileGet(req, args):
    (path, content_type) = args
    if req.verb != request.HTTP_GET:
        return HttpResponse(400)
    logger.info(f"Processing GET on {path}, returning file contents")
    f = open(path, "rb")
    resp = HttpResponse(200)
    resp.setByteContent(f.read(), content_type)
    return resp
