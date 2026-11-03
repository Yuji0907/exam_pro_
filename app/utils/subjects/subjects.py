import json
from database.db_manager import DBManager
from repositories.subject_repo import SubjectRepository 
# from utils.willayas import 
import os
SUBJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
SUBJECTS=None
with open(os.path.join(SUBJECT_FOLDER,"subjects_data.json"), "r", encoding="utf-8") as f:
    SUBJECTS = json.load(f)


def insert_all_subjects(session):
    subject_repo = SubjectRepository(session)
    for key in SUBJECTS.keys():
        subject_repo.create(key,SUBJECTS[key]["subject"],SUBJECTS[key]["coeff"])
        
# def insert_subject(session,key):
#         global SUBJECTS
#         SubjectRepository.create(key,SUBJECTS[key])
