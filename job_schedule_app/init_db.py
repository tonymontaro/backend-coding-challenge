from fastapi import Depends
from sqlalchemy.orm import Session
import json
import datetime

from . import schemas


def load_data_into_db(db: Session, file_path: str):
    with open(file_path, 'r') as f:
        # with open("planning.json", 'r') as f:
        data = json.load(f)
        for d in data:
            schemas.Office.create(db, schemas.OfficeCreate(
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
                office_id=d["officePostalCode"]
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
                schemas.Skill.create(db, db_skill, db_job.original_id)

            for skill in d["optionalSkills"]:
                db_skill = schemas.SkillCreate(
                    name=skill["name"], category=skill["category"])
                schemas.OptionalSkill.create(db, db_skill, db_job.original_id)

            db.commit()
