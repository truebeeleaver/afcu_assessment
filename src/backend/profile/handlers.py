import logging
import json

import backend.server.request as request
import backend.server.util as sutil
import backend.profile.util as putil
import backend.profile.session as session

from backend.server.response import HttpResponse

logger = logging.getLogger(__name__)


# Log in to specified profile, switching accounts if we are already logged in
def handleLogin(req, args):
    logger.info(f"Processing {req.verb} on login resource")
    (profiles, sessions) = args

    putil.assertValidVerb(req, {request.HTTP_POST})
    putil.assertContentType(req, "application/json")

    content = putil.getJsonContent(req)

    if "username" not in content or "password" not in content:
        # Missing required fields
        raise sutil.HttpException(400, "Expected username and password fields")
    username = content["username"]
    password = content["password"]
    
    resp = HttpResponse(201)

    (session_id, profile) = sessions.getSessionIDAndProfile(req, resp)
    profile = sessions.authenticateSession(profiles, session_id, username, password)
    if not profile:
        # Don't raise here--we want to return the same response as we might have a cookie now
        resp.status = 401

    return resp


# Create and log in to profile
def handleSignup(req, args):
    logger.info(f"Processing {req.verb} on signup resource")
    (profiles, sessions) = args

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

    (session_id, profile) = sessions.getSessionIDAndProfile(req, resp)
    
    # if we are already authenticated, that's fine--make a new profile and log in as that user
    profile = profiles.register(username, password, phone)
    sessions.authenticateSession(profiles, session_id, username, password)

    return resp


# Return profile data
def handleProfile(req, args):
    logger.info(f"Processing {req.verb} on profile resource")
    (profiles, sessions) = args

    putil.assertValidVerb(req, {request.HTTP_GET})

    resp = HttpResponse(200)

    (session_id, profile) = sessions.getSessionIDAndProfile(req, resp)

    if not profile:
        # Don't raise here--we want to return the same response as we might have a cookie now
        resp.status = 401
    else:
        data = {}
        data["username"] = profile.user
        data["phone"] = profile.phone
        resp.setTextContent(json.dumps(data), "application/json")

    return resp


