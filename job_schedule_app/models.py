from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
from .database import Base
from sqlalchemy.orm import validates, relationship
# import uuid

# Base = declarative_base()


class TalentOrm(Base):
    __tablename__ = 'talents'

    id = Column(String, primary_key=True)
    name = Column(String)
    grade = Column(String)


class SkillOrm(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    job = relationship("JobOrm", back_populates="required_skills")


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
    optional_skills = Column(String)
    is_unassigned = Column(Boolean)
    talent_id = Column(String)
    required_skills = relationship("SkillOrm", back_populates="job")


class City(Base):
    __tablename__ = 'cities'

    city = Column(String)
    postal_code = Column(String, primary_key=True)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(String, primary_key=True)
    name = Column(String)
    industry = Column(String)
