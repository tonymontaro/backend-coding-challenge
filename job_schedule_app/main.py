from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import json

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
        data = json.load(f)
        for d in data:
            if (d["talentId"] != ""):
                talent = schemas.TalentCreate(
                    id=d["talentId"],  name=d["talentName"], grade=d["talentGrade"])
                schemas.Talent.create(db, talent)


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    load_data_into_db(db)
    return {"Hello": "World"}


@app.get("/create")
def read_root(db: Session = Depends(get_db)) -> schemas.Talent:
    talent = schemas.TalentCreate(name="Tony", grade="23")
    return schemas.Talent.create(db, talent)


@app.get("/talents")
def get_talents(db: Session = Depends(get_db)) -> list[schemas.Talent]:
    talents = [schemas.Talent.from_orm(talent)
               for talent in db.query(models.TalentOrm).all()]
    return talents
