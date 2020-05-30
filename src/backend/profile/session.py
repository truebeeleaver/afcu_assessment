import logging
import uuid
import hashlib

from backend.profile.manager import ProfileManager

logger = logging.getLogger(__name__)

SESSION_COOKIE = "session_token"

def sessionIDToLog(session_id):
    # We really shouldn't be logging out user session cookies, but we want stable IDs
    return hashlib.md5(bytes(session_id, "utf-8")).hexdigest()

class SessionManager:
    def __init__(self):
        logger.info("Initializing session manager")
        self.sessions = {}

    def generateCookie(self):
        # probably overkill to use a uuid
        return str(uuid.uuid4())

    # Get or create session id for this request, set cookie if necessary
    # Return profile for authenticated sessions, or None
    def getSessionIDAndProfile(self, req, resp):
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
                logger.info(f"Authenticated as user {profile.user}")
        return (cookie, profile)

    def authenticateSession(self, profiles, session_id, username, password):
        profile = profiles.getProfileWithPassword(username, password)
        if profile:
            if self.sessions[session_id]:
                logger.info(f"Disassociating user {self.sessions[session_id].user} from session {sessionIDToLog(session_id)}")
            logger.info(f"Associating user {profile.user} from session {sessionIDToLog(session_id)}")
            self.sessions[session_id] = profile
        return profile
