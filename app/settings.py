import os

ENVIRONMENT = "unknown"
try:
    if os.environ["SERVER_SOFTWARE"].lower().startswith("dev"):
        ENVIRONMENT = "local"
    elif os.environ["SERVER_SOFTWARE"].lower().startswith("google apphosting"):
        ENVIRONMENT = "hosted"
except:
    pass

DEBUG = (ENVIRONMENT == "local")


CACHE           = not DEBUG
CACHE_LIFE      = 1800  # num seconds to cache stuff
THROTTLE_API    = True
THROTTLE_LIFE   = 60    # num seconds per IP per request

VERSION = os.environ['CURRENT_VERSION_ID']

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')



# Import secrets, like:
# SKELETON_KEY = ""

try:
    from secrets import *
except ImportError:
    pass