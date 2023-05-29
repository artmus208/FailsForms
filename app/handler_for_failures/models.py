from app import db
from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime, Integer, String, or_, and_

# Done:
# [X]: Создать в модель в БД
# [x]: Сделать выгрузку всех пустых записей

# TODO:
class MyBaseClass:
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def commit(self):
        db.session.commit()

    @classmethod
    def get(cls, id):
        try:
            return db.session.get(cls, id)
        except Exception:
            db.session.rollback()
            raise





class ArchivesCrusherFailures(MyBaseClass, db.Model):
    id = Column(Integer, primary_key=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    crusher_id = Column(Integer)
    fault = Column(String(255))
    
    def __init__(self, crusher_id=0, fail=''):
        self.crusher_id = crusher_id
        self.fault = fail

    def __repr__(self):
        return f'{self.id},{self.time_created},{self.time_updated},{self.crusher_id},{self.fault}'

    def as_dict(self):
        d = dict(zip(['id', 'time_created', 'time_updated', 'crusher_id', 'fault'],
                    [self.id, self.time_created.strftime("%d.%m.%Y %H:%M"), 
                    self.time_updated.strftime("%d.%m.%Y %H:%M"), self.crusher_id, self.fault]))
        return d

    @classmethod
    def get_unfilled_faults(cls):
        res = db.session.execute(
            db.select(cls).where(or_(cls.fault == None, cls.fault == ''))
            .order_by(cls.time_created.desc())
            ).scalars()
        return res.all()
    

    @classmethod
    def get_filled_faults(cls):
        # [x]: Сортировать полученный список в порядке возрастания даты
        res = db.session.execute(
            db.select(cls).where(and_(cls.fault != None, cls.fault != ''))
            .order_by(cls.time_created)
            ).scalars()
        res = res.all()[::-1]
        return res

    @classmethod
    def get_first_empty(cls):
        res = db.session.execute(
            db.select(cls).where(or_(cls.fault == None,cls.fault == ''))
        ).scalar()
        return res

