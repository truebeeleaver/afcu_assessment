import logging

logger = logging.getLogger(__name__)

class ProfileError(Exception):
    def __init__(self, errors):
        self.errors = errors
    
    def __str__(self):
        return f"ProfileError {self.errors}"

class Profile:
    def __init__(self, email, password, phone):
        self.email = email
        # TODO store hash of salted password!
        # NB: I would not ever write crypto code myself, but to simplify setup of this project I don't want to use scrypt either
        self.password = password
        self.phone = phone

def validateEmail(address):
    # Don't get too in the weeds here--just check for '@' and a domain
    # Honestly the only real validation is to try to send mail.
    if not address:
        return False
    parts = address.split('@')
    if len(parts) != 2 or '.' not in parts[1]:
        return False
    return True

def validatePassword(password):
    if not password or password == 'swordfish':
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


    def register(self, email, password, phone):
        errors = {}

        if email in self.profiles:
            errors["email"] = "Email is unavailable"
        elif not validateEmail(email):
            errors["email"] = "Email address is not valid"

        if not validatePassword(password):
            errors["password"] = "Insufficiently strong password"

        if not validatePassword(phone):
            errors["phone"] = "Invalid phone number"

        # Return complete set of validation errors
        if errors:
            raise ProfileError(errors)

        profile = Profile(email, password, phone)
        self.profiles[email] = profile

        return profile

    def getProfile(self, email):
        return self.profiles.get(email)

    def getProfileWithPassword(self, email, password):
        profile = self.profiles.get(email)
        if profile:
            if profile.password == password:
                return profile
        if not profile:
            logger.warn(f"Invalid login attempt for user {email}")
        return None

