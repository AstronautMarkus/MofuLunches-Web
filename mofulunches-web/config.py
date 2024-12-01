import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "astronautmarkuswasherelmao"
    DEBUG = True

config = Config()
