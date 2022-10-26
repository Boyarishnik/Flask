import os
import sys
from pprint import pprint


class Config:
    SECRET_KEY = os.environ.get("SECRET KEY") or "lkjhgfdscvbnjuytfvbnjuytrfcvbnjy"
    DEBUG = True
    DATABASE = "flaskdb.db"


# print(sys.path)
