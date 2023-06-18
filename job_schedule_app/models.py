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


class JobsOrm(Base):
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
    required_skills = Column(String)
    optional_skills = Column(String)
    is_unassigned = Column(Boolean)
    # talent = relationship("TalentOrm")


class City(Base):
    __tablename__ = 'cities'

    city = Column(String)
    postal_code = Column(String, primary_key=True)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(String, primary_key=True)
    name = Column(String)
    industry = Column(String)


class Skills(Base):
    __tablename__ = 'skills'

    name = Column(String, primary_key=True)
    category = Column(String, nullable=False)

    # @validates('category')
    # def validate_category(self, key, value):
    #     if not value:
    #         raise ValueError("Category field is required")
    #     return value
