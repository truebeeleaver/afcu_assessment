import logging
import json

import backend.server.request as request
import backend.server.util as sutil
import backend.profile.util as putil

from backend.server.response import HttpResponse

logger = logging.getLogger(__name__)


def handleLogin(req, profiles):
    logger.info(f"Processing {req.verb} on login resource")

    putil.assertValidVerb(req, {request.HTTP_POST})
    putil.assertContentType(req, "application/json")

    content = putil.getJsonContent(req)

    if "username" not in content or "password" not in content:
        # Missing required fields
        raise sutil.HttpException(400, "Expected username and password fields")
    username = content["username"]
    password = content["password"]
    
    resp = HttpResponse(201)

    # TODO handle login

    return resp


def handleSignup(req, profiles):
    logger.info(f"Processing {req.verb} on signup resource")

    putil.assertValidVerb(req, {request.HTTP_POST})
    putil.assertContentType(req, "application/json")

    content = putil.getJsonContent(req)
    if (
        "username" not in content
        or "password" not in content
        or "phone" not in content
    ):
        # Missing required fields
        raise sutil.HttpException(
            400, "Expected username, password, and phone fields"
        )
    username = content["username"]
    password = content["password"]
    phone = content["phone"]

    resp = HttpResponse(201)

    # TODO signup

    return resp


def handleProfile(req, profiles):
    logger.info(f"Processing {req.verb} on profile resource")

    putil.assertValidVerb(req, {request.HTTP_GET})

    resp = HttpResponse(200)

    # TODO profile

    return resp


class ProfileManager:
    def __init__(self):
        pass
