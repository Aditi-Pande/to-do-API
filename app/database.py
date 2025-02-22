import time
from . import db

def db_connection(app):
    retries = 5
    while retries:
        try:
            with app.app_context():
                db.create_all()
            print("Database is ready.")
            return
        except Exception as e:
            print(f"Database not ready, retrying... ({retries} attempts left)")
            time.sleep(5)
            retries -= 1
    print("Could not connect to the database.")
