from dotenv import load_dotenv
from database.db_manager import DBManager
import os
from utils.willayas.wilaya import insert_wilayas 
from utils.subjects.subjects import insert_all_subjects
load_dotenv()
database_connection_string = os.getenv("DB_CONNECTION_STRING")

from utils.candidates.import_candidates import import_random_candidates


if __name__ == "__main__":
    db = DBManager(database_connection_string)
    session = db.get_session()
    # db.create_all_tables()
    # insert_all_subjects(session)
    insert_wilayas(session)
    # import_random_candidates(session)


print("finished")
