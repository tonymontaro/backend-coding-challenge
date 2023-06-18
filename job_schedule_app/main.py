from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import json
import datetime

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def load_data_into_db(db: Session):
    with open("job_schedule_app/test.json", 'r') as f:
        # with open("job_schedule_app/planning.json", 'r') as f:
        data = json.load(f)
        for d in data:

            office = schemas.Office.create(db, schemas.OfficeCreate(
                city=d["officeCity"], postal_code=d["officePostalCode"]))
            job = schemas.JobCreate(
                original_id=d["originalId"],
                booking_grade=d["bookingGrade"],
                operating_unit=d["operatingUnit"],
                job_manager_id=d["jobManagerId"],
                job_manager_name=d["jobManagerName"],
                total_hours=d["totalHours"],
                start_date=datetime.datetime.strptime(
                    d["startDate"], "%m/%d/%Y %I:%M %p"),
                end_date=datetime.datetime.strptime(
                    d["endDate"], "%m/%d/%Y %I:%M %p"),
                required_skills=d["talentId"],
                optional_skills=d["talentId"],
                is_unassigned=d["isUnassigned"],
                client_id=d["clientId"],
                office_id=office.id
            )
            if (d["talentId"] != ""):
                talent = schemas.TalentCreate(
                    id=d["talentId"],  name=d["talentName"], grade=d["talentGrade"])
                schemas.Talent.create(db, talent)
                job.talent_id = d["talentId"]
            client = schemas.ClientCreate(
                id=d["clientId"], name=d["clientName"], industry=d["industry"]
            )
            schemas.Client.create(db, client)

            db_job = schemas.Job.create(db, job)

            for skill in d["requiredSkills"]:
                db_skill = schemas.SkillCreate(
                    name=skill["name"], category=skill["category"])
                schemas.Skill.create(db, db_skill, db_job.id)

            for skill in d["optionalSkills"]:
                db_skill = schemas.SkillCreate(
                    name=skill["name"], category=skill["category"])
                schemas.OptionalSkill.create(db, db_skill, db_job.id)


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    load_data_into_db(db)
    return {"Hello": "World"}


@app.get("/create")
def read_root(db: Session = Depends(get_db)):
    office = schemas.OfficeCreate(city="tokyo", postal_code="123")
    of = schemas.Office.create(db, office)
    return of


@app.get("/talents")
def get_talents(db: Session = Depends(get_db)) -> list[schemas.Talent]:
    talents = [schemas.Talent.from_orm(talent)
               for talent in db.query(models.TalentOrm).offset(0).limit(100).all()]
    return talents


@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)) -> list[schemas.Job]:
    jobs = [schemas.Job.from_orm(job)
            for job in db.query(models.JobOrm).offset(0).limit(10).all()]
    # print(jobs)
    return jobs
