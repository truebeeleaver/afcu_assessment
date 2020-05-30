import logging
import sys
import getopt

from backend.server.request import HttpRequest
from backend.server.response import HttpResponse
from backend.server.server import Server
from backend.server.file import handleFileGet
from backend.profile.handlers import handleLogin, handleSignup, handleProfile, handleLogout
from backend.profile.manager import ProfileManager
from backend.profile.session import SessionManager

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
    sessions = SessionManager()

    # set handlers for our resources; ideally this would be in a config ie pyramid but this is a toy server
    server.bindResource("/api/profile/login", handleLogin, (profiles, sessions))
    server.bindResource("/api/profile/signup", handleSignup, (profiles, sessions))
    server.bindResource("/api/profile", handleProfile, (profiles, sessions))
    server.bindResource("/api/profile/logout", handleLogout, (profiles, sessions))

    # set handlers for our raw HTML/CSS/JS implementation, to get files
    server.bindResource("/profile", handleFileGet, ("frontend/profile.html", "text/html; charset=utf-8"))
    server.bindResource("/profile.js", handleFileGet, ("frontend/profile.js", "application/javascript; charset=utf-8"))
    server.bindResource("/login", handleFileGet, ("frontend/login.html", "text/html; charset=utf-8"))
    server.bindResource("/login.js", handleFileGet, ("frontend/login.js", "application/javascript; charset=utf-8"))
    server.bindResource("/signup", handleFileGet, ("frontend/signup.html", "text/html; charset=utf-8"))
    server.bindResource("/signup.js", handleFileGet, ("frontend/signup.js", "application/javascript; charset=utf-8"))
    server.bindResource("/styles.css", handleFileGet, ("frontend/styles.css", "text/css; charset=utf-8"))

    server.run()

    logger.info("Server shutting down normally")

