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


class SkillBase(BaseModel):
    name: str
    category: str


class SkillCreate(SkillBase):
    pass


class Skill(SkillBase):
    id: int
    job_id: int

    def create(db: Session, skill: SkillCreate, job_id: int):
        new_skill = models.SkillOrm(**skill.dict(), job_id=job_id)
        db.add(new_skill)
        db.commit()
        db.refresh(new_skill)
        return Skill.from_orm(new_skill)

    class Config:
        orm_mode = True


class JobBase(BaseModel):
    original_id: str
    booking_grade: str
    operating_unit: str
    job_manager_name: str
    job_manager_id: str
    total_hours: float
    start_date: datetime
    end_date: datetime
    optional_skills: str
    is_unassigned: bool
    talent_id: str | None = None


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    required_skills: list[Skill] = []

    def get(db: Session, original_id: str):
        return db.query(models.JobOrm).filter(models.JobOrm.original_id == original_id).first()

    def create(db: Session, job: JobCreate):
        new_job = models.JobOrm(**job.dict())
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return Job.from_orm(new_job)

    class Config:
        orm_mode = True
