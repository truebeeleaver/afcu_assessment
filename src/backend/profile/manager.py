import logging

logger = logging.getLogger(__name__)

class ProfileError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return f"ProfileError {self.message}"

class Profile:
    def __init__(self, user, pwd, phone):
        self.user = user
        # TODO store hash of salted password!
        # NB: I would not ever write crypto code myself, but to simplify setup of this project I don't want to use scrypt either
        self.pwd = pwd 
        self.phone = phone

class ProfileManager:
    def __init__(self):
        logger.info("Initializing profile manager")
        self.profiles = {}

        # TODO get rid of this sample data once we have perstitence
        self.profiles["foo@example.com"] = Profile("foo@example.com", "bar", "8675309")

    def register(self, user, pwd, phone):
        if user in self.profiles:
            raise ProfileError(f"Username {user} is unavailable")

        # TODO validate username is an email
        # TODO validate password strength?
        # TODO validate phone

        profile = Profile(user, pwd, phone)
        self.profiles[user] = profile

        return profile

    def getProfile(self, user):
        return self.profiles.get(user)

    def getProfileWithPassword(self, user, password):
        profile = self.profiles.get(user)
        if profile:
            if profile.pwd == password:
                return profile
        if not profile:
            logger.warn(f"Invalid login attempt for user {user}")
        return None

