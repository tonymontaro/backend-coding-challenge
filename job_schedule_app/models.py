from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey

from .database import Base
from sqlalchemy.orm import validates, relationship, Mapped


class TalentOrm(Base):
    __tablename__ = 'talents'

    id = Column(String, primary_key=True)
    name = Column(String)
    grade = Column(String)


class BaseSkillOrm():
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)


class SkillOrm(Base, BaseSkillOrm):
    __tablename__ = 'require_skills'
    job_id = Column(String, ForeignKey("jobs.original_id"))
    job = relationship("JobOrm", back_populates="required_skills")


class OptionalSkillOrm(Base, BaseSkillOrm):
    __tablename__ = 'optional_skills'
    job_id = Column(String, ForeignKey("jobs.original_id"))
    job = relationship("JobOrm", back_populates="optional_skills")


class ClientOrm(Base):
    __tablename__ = 'clients'

    id = Column(String, primary_key=True)
    name = Column(String)
    industry = Column(String)


class OfficeOrm(Base):
    __tablename__ = 'offices'

    city = Column(String)
    postal_code = Column(String, primary_key=True)


class JobOrm(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    original_id = Column(String, unique=True, nullable=False)
    booking_grade = Column(String)
    operating_unit = Column(String, nullable=False)
    job_manager_name = Column(String)
    job_manager_id = Column(String)
    total_hours = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_unassigned = Column(Boolean)
    talent_id = Column(String, ForeignKey("talents.id"))
    talent: Mapped["TalentOrm"] = relationship()
    client_id = Column(String, ForeignKey("clients.id"))
    client: Mapped["ClientOrm"] = relationship()
    office_id = Column(Integer, ForeignKey("offices.postal_code"))
    office: Mapped["OfficeOrm"] = relationship()
    required_skills = relationship("SkillOrm", back_populates="job")
    optional_skills = relationship("OptionalSkillOrm", back_populates="job")
