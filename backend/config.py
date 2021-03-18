import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')

TELEGRAM_TIMEZONE = os.environ.get('TELEGRAM_TIMEZONE')
LOCAL_TIMEZONE = os.environ.get('LOCAL_TIMEZONE')
