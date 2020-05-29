import logging

from backend.server.request import HttpRequest
from backend.server.response import HttpResponse
from backend.server.server import Server
from backend.profile.profile import handleLogin, handleSignup, handleProfile, ProfileManager

logger = logging.getLogger(__name__)

def hello_world(req, state):
    resp = HttpResponse(200)
    resp.setTextContent("<html><body><h1>Hello World</h1></body></html>", "text/html")
    return resp

# this will be our entrypoint
if __name__ == "__main__":
    logging.basicConfig(
        filename="backend.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s",
    )
    logger.info("Server starting up")

    #TODO move to config file
    server = Server("127.0.0.1", 8080)
    profiles = ProfileManager()

    # set handlers for our resources; ideally this would be in a config ie pyramid but this is a toy server
    server.bindResource("/helloworld", hello_world, None)
    server.bindResource("/profile/login", handleLogin, profiles)
    server.bindResource("/profile/signup", handleSignup, profiles)
    server.bindResource("/profile", handleProfile, profiles)

    server.run()

    logger.info("Server shutting down normally")

