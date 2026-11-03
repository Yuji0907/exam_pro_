from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.orm_models import Willaya,CodeFormat,Subject,Subject_to_grade,Code,Candidate,Eval,Packet,Center,CenterAssignment,Grade
# CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
# ROOT_PATH = os.path.dirname(CURRENT_PATH)
# ENV_PATH = os.path.join(ROOT_PATH,".env")




class DBManager:
    def __init__(self,db_url):
        self.engine = create_engine(db_url,echo=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_all_tables(self):
        print("==============================willaya====================")
        Willaya.__table__.create(self.engine)
        print("==============================Grade====================")
        Grade.__table__.create(self.engine)
        print("==============================Center====================")
        Center.__table__.create(self.engine)
        print("==============================CenterAssignment====================")
        CenterAssignment.__table__.create(self.engine)

        print("==============================Subject====================")
        Subject.__table__.create(self.engine)
        print("==============================CodeFormat====================")
        CodeFormat.__table__.create(self.engine)
        print("==============================Subject_to_grade====================")
        Subject_to_grade.__table__.create(self.engine)
        print("==============================Packet====================")
        Packet.__table__.create(self.engine)
        print("==============================Candidate====================")
        Candidate.__table__.create(self.engine)
        print("==============================Code====================")
        Code.__table__.create(self.engine)
        print("==============================Eval====================")
        Eval.__table__.create(self.engine)
        

        pass

    def get_session(self):
        return self.SessionLocal()