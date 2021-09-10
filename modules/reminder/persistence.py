from tinydb import TinyDB, Query
from tinydb.operations import add, subtract

users_db = TinyDB('./db/reminders.json')

class DBReminders:
    def __init__(self, user_id):
        pass

    @staticmethod
    def get_user(user_id):
        pass