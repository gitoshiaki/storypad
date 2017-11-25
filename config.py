import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

DB_NAME = 'spd_test.db'
DB_PATH = os.path.join(ROOT_PATH, DB_NAME)
DB_URL  = 'sqlite:///{database}'.format(database=DB_PATH)
