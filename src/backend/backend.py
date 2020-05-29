import logging
import sys
import getopt

from backend.server.request import HttpRequest
from backend.server.response import HttpResponse
from backend.server.server import Server
from backend.profile.profile import handleLogin, handleSignup, handleProfile, ProfileManager

logger = logging.getLogger(__name__)

def print_usage():
    print("backend.py -a <address> -p <port>")

# this will be our entrypoint
if __name__ == "__main__":
    logging.basicConfig(
        filename="backend.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s",
    )
    logger.info("Server starting up")

    ip_addr = "127.0.0.1"
    port = 8080

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "ha:p:",["address=", "port="])
    except getopt.GetOptError:
        print_usage()
        sys.exit(1)
    for opt, arg in opts:
        if opt == "-h":
            print_usage()
        elif opt in ("-a", "--addr"):
            ip_addr = arg
        elif opt in ("-p", "--port"):
            port = int(arg)

    # instantiate server and profile manager
    server = Server(ip_addr, port)
    profiles = ProfileManager()

    # set handlers for our resources; ideally this would be in a config ie pyramid but this is a toy server
    server.bindResource("/profile/login", handleLogin, profiles)
    server.bindResource("/profile/signup", handleSignup, profiles)
    server.bindResource("/profile", handleProfile, profiles)

    server.run()

    logger.info("Server shutting down normally")

