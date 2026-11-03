from sqlalchemy.orm import Session
from database.orm_models import Willaya as WillayaORM
from models.willaya_model import WillayaModel

class WillayaRepository:
    def __init__(self, session: Session):
        self.session = session

    # fetching
    def get_all(self)-> list[WillayaModel]:
        orm_res = self.session.query(WillayaORM).all()
        return [self._to_model(x) for x in orm_res]

    def get_by_id(self,id:int)-> WillayaModel | None:
        orm_res = self.session.get(WillayaORM,(id))
        return self._to_model(orm_res) if orm_res else None

    def get_by_willaya(self,willaya:str)->WillayaModel |  None:
        orm_res = self.session.get(WillayaORM,(willaya))
        return self._to_model(orm_res) if orm_res else None



    #create 
    def create(self,
            id:int,
            willaya: str,
    ) -> WillayaModel | bool:    
        existing = self.get_by_id(id)
        if existing:
            return False
        
        willaya_ =WillayaORM(id=id,willaya=willaya)
        self.session.add(willaya_)
        self.session.commit()
        self.session.refresh(willaya_)
        return self._to_model(willaya_)

    def _to_model(self, orm_willaya: WillayaORM) -> WillayaModel:
        return WillayaModel(
            orm_willaya.id,
            orm_willaya.willaya
        )