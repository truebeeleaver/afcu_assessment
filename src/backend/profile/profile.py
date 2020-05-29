import logging

from backend.server.request import HttpRequest
from backend.server.response import HttpResponse

logger = logging.getLogger(__name__)

def handleLogin(req, profiles):
    logger.info(f"Processing {req.verb} on login resource")
    if req.verb != "POST":
        # Invalid verb
        return HttpResponse(400)
    resp = HttpResponse(201)

    # TODO login

    return resp

def handleSignup(req, profiles):
    logger.info(f"Processing {req.verb} on signup resource")
    if req.verb != "POST":
        # Invalid verb
        return HttpResponse(400)
    resp = HttpResponse(201)

    # TODO signup

    return resp

def handleProfile(req, profiles):
    logger.info(f"Processing {req.verb} on profile resource")
    if req.verb != "GET":
        # Invalid verb
        return HttpResponse(400)
    resp = HttpResponse(200)

    # TODO profile 

    return resp

class ProfileManager:
    def __init__(self):
        pass
