import json
from database.db_manager import DBManager
from repositories.willaya_repo import WillayaRepository
# from utils.willayas import 
import os
WILLAYA_FOLDER = os.path.dirname(os.path.abspath(__file__))
print()
WILAYAS=None
with open(os.path.join(WILLAYA_FOLDER,"wilaya_data.json"), "r", encoding="utf-8") as f:
    WILAYAS = json.load(f)


def insert_wilayas(session):
    willaya_repo = WillayaRepository(session)
    for key in WILAYAS.keys():
        print("==========")
        print(key)
        willaya_repo.create(key,WILAYAS[key])
        
def insert_wilaya(session,key):
        global WILAYAS
        WillayaRepository.create(key,WILAYAS[key])
