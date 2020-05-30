import json

import backend.server.request as request
import backend.server.util as sutil
from backend.server.response import HttpResponse


def assertValidVerb(req, verbs):
    if req.verb not in verbs:
        # Invalid verb
        raise sutil.HttpException(
            400,
            f"Unacceptable verb {req.verb}, valid verbs for this resource are {verbs}",
        )
    return None


def assertContentType(req, content_type):
    if (
        "content-type" not in req.headers
        or req.headers["content-type"] != content_type
    ):
        raise sutil.HttpException(
            400, f"Unacceptable content type. Expected {content_type}"
        )
    return None


def getJsonContent(req):
    try:
        return json.loads(str(req.content, "utf8"))
    except json.decoder.JSONDecodeError as e:
        raise sutil.HttpException(400, f"Invalid JSON: {str(e)}; content={str(req.content)}")
