from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from . import models


class TalentBase(BaseModel):
    id: str
    name: str
    grade: str | None = None


class TalentCreate(TalentBase):
    pass


class Talent(TalentBase):
    def get(db: Session, id: str):
        return db.query(models.TalentOrm).filter(models.TalentOrm.id == id).first()

    def create(db: Session, talent: TalentCreate):
        existing = Talent.get(db, talent.id)
        if existing:
            return Talent.from_orm(existing)
        new_talent = models.TalentOrm(**talent.dict())
        db.add(new_talent)
        db.commit()
        db.refresh(new_talent)
        return Talent.from_orm(new_talent)

    class Config:
        orm_mode = True


class JobsBase(BaseModel):
    original_id: str
    booking_grade: str
    operating_unit: str
    job_manager_name: str
    job_manager_id: str
    total_hours: float
    start_date: datetime
    end_date: datetime
    required_skills: str
    optional_skills: str
    is_unassigned: bool
