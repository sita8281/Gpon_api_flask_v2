from flask import Flask
from .profile_handler import ProfilesStorage
import logging
import os.path


app_path = os.path.abspath(__name__)  # base app dir
firmware_version = 0.01
prof_manager = ProfilesStorage(file_path=os.path.join(app_path, 'profiles/profiles.pickle'))
logging.basicConfig(filename=os.path.join(app_path, 'logs/logs.txt'), level=logging.DEBUG)
app = Flask(__name__)

from app import routes


