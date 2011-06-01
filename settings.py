import os

CACHE = False
CACHE_LIFE = 1800
THROTTLE_API = True
THROTTLE_LIFE = 60

VERSION = os.environ['CURRENT_VERSION_ID']

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

ENVIRONMENT = "unknown"
try:
    if os.environ["SERVER_SOFTWARE"].lower().startswith("dev"):
        ENVIRONMENT = "local"
    elif os.environ["SERVER_SOFTWARE"].lower().startswith("google apphosting"):
        ENVIRONMENT = "hosted"
except:
    pass

DEBUG = (ENVIRONMENT == "local")


# Import secrets, like:
# DATA_KEY = ""

try:
    from secrets import *
except ImportError:
    pass