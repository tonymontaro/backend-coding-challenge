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
        return Skill.from_orm(new_skill)

    class Config:
        orm_mode = True


class OptionalSkill(SkillBase):
    id: int
    job_id: int

    def create(db: Session, skill: SkillCreate, job_id: int):
        new_skill = models.OptionalSkillOrm(**skill.dict(), job_id=job_id)
        db.add(new_skill)
        db.commit()
        return OptionalSkill.from_orm(new_skill)

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    id: str
    name: str
    industry: str


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    def get(db: Session, id: str):
        return db.query(models.ClientOrm).filter(models.ClientOrm.id == id).first()

    def create(db: Session, client: ClientCreate):
        existing = Client.get(db, client.id)
        if existing:
            return Client.from_orm(existing)
        new_client = models.ClientOrm(**client.dict())
        db.add(new_client)
        db.commit()
        return Client.from_orm(new_client)

    class Config:
        orm_mode = True


class OfficeBase(BaseModel):
    city: str | None = None
    postal_code: str


class OfficeCreate(OfficeBase):
    pass


class Office(OfficeBase):
    id: int

    def get(db: Session, postal_code: str):
        return db.query(models.OfficeOrm).filter(models.OfficeOrm.postal_code == postal_code).first()

    def create(db: Session, office: OfficeCreate):
        existing = Office.get(db, office.postal_code)
        if existing:
            return Office.from_orm(existing)
        new_office = models.OfficeOrm(**office.dict())
        db.add(new_office)
        db.commit()
        db.refresh(new_office)
        return Office.from_orm(new_office)

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
    is_unassigned: bool
    client_id: str
    talent_id: str | None = None
    office_id: int


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    required_skills: list[Skill] = []
    optional_skills: list[OptionalSkill] = []
    talent: Talent | None = None
    client: Client | None = None
    office: Office | None = None

    def get(db: Session, original_id: str):
        return db.query(models.JobOrm).filter(models.JobOrm.original_id == original_id).first()

    def create(db: Session, job: JobCreate):
        new_job = models.JobOrm(**job.dict())
        db.add(new_job)
        db.commit()
        return Job.from_orm(new_job)

    class Config:
        orm_mode = True
