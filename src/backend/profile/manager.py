import logging

logger = logging.getLogger(__name__)

class ProfileError(Exception):
    def __init__(self, errors):
        self.errors = errors
    
    def __str__(self):
        return f"ProfileError {self.errors}"

class Profile:
    def __init__(self, user, pwd, phone):
        self.user = user
        # TODO store hash of salted password!
        # NB: I would not ever write crypto code myself, but to simplify setup of this project I don't want to use scrypt either
        self.pwd = pwd 
        self.phone = phone

def validateAddress(address):
    # Don't get too in the weeds here--just check for '@' and a domain
    # Honestly the only real validation is to try to send mail.
    if not address:
        return False
    parts = address.split('@')
    if len(parts) != 2 or '.' not in parts[1]:
        return False
    return True

def validatePassword(pwd):
    if not pwd or pwd == 'swordfish':
        return False
    return True

def validatePhone(phone):
    # No sense in even trying to validate a phone number. US with extensions is crazy enough
    if not phone:
        return False
    return True

class ProfileManager:
    def __init__(self):
        logger.info("Initializing profile manager")
        self.profiles = {}

        # TODO get rid of this sample data once we have perstitence
        self.profiles["foo@example.com"] = Profile("foo@example.com", "bar", "8675309")

    def register(self, user, pwd, phone):
        errors = {}

        if user in self.profiles:
            errors["username"] = "Username is unavailable"
        elif not validateAddress(user):
            errors["username"] = "Username is not a valid email address"

        if not validatePassword(pwd):
            errors["password"] = "Insufficiently strong password"

        if not validatePassword(phone):
            errors["phone"] = "Invalid phone number"

        # Return complete set of validation errors
        if errors:
            raise ProfileError(errors)

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

