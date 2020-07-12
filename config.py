import os
HOME_DIR = os.path.dirname(os.path.realpath(__file__))

DATA_DIR = os.path.join(HOME_DIR, r"data/")

# URL exclusions
EXCLUDED_URL_EXTENSIONS = ["application", "audio", "video", "image"]

USE_PROXY_SERVER = False
