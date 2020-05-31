import logging
import uuid
import hashlib
from threading import RLock

from backend.profile.manager import ProfileManager, Profile

logger = logging.getLogger(__name__)

SESSION_COOKIE = "session_token"

def sessionIDToLog(session_id):
    # Do not log out cookies
    return hashlib.md5(bytes(session_id, "utf-8")).hexdigest()

class SessionManager:
    def __init__(self):
        logger.info("Initializing session manager")
        self.sessions = {}
        self.lock = RLock()

    def generateCookie(self):
        # probably overkill to use a uuid
        return str(uuid.uuid4())

    # Get or create session id for this request, set cookie if necessary
    # Return profile for authenticated sessions, or None
    def getSessionIDAndProfile(self, req, resp):
        with self.lock:
            cookie = req.getCookie(SESSION_COOKIE)
            if not cookie or not cookie in self.sessions:
                # Generate a new unauthenticated session
                cookie = self.generateCookie()
                self.sessions[cookie] = None
                profile = None
                logger.info(f"Created session {sessionIDToLog(cookie)}")
                resp.setHeader("Set-Cookie", f"{SESSION_COOKIE}={cookie}; SameSite=Strict")
            elif cookie in self.sessions:
                profile = self.sessions[cookie]
                logger.info(f"Attached to session {sessionIDToLog(cookie)}")
                if profile:
                    logger.info(f"Authenticated as user {profile.email}")
            return (cookie, profile)

    def authenticateSession(self, profiles, session_id, email, password):
        with self.lock:
            profile = profiles.getProfileWithPassword(email, password)
            if profile:
                if self.sessions[session_id]:
                    logger.info(f"Disassociating user {self.sessions[session_id].email} from session {sessionIDToLog(session_id)}")
                logger.info(f"Associating user {profile.email} to session {sessionIDToLog(session_id)}")
                self.sessions[session_id] = profile
            return profile

    def logoutSession(self, req):
        with self.lock:
            cookie = req.getCookie(SESSION_COOKIE)
            if cookie and cookie in self.sessions:
                self.sessions[cookie] = None
