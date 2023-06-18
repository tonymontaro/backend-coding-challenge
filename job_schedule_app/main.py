from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
import json
import datetime

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from . import crud, models, schemas
from .database import SessionLocal, engine
from .init_db import load_data_into_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/initDatabase")
async def read_root(db: Session = Depends(get_db), isTest: str = ""):
    if isTest == "true":
        load_data_into_db(db, "job_schedule_app/test.json")
    else:
        load_data_into_db(db, "planning.json")
    return {"message": "Completed"}


@app.get("/jobs")
async def get_jobs(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=0, lt=101),
    offset: int = Query(0, ge=0),
    filterByTalentId="",
    filterByClientId="",
    orderByManagertName: str = Query("", description="options: [asc, desc]"),
    searchByOperatingUnit: str = "",
):
    query = db.query(models.JobOrm)
    total = query.count()
    if (filterByTalentId != ""):
        query = query.filter(models.JobOrm.talent_id == filterByTalentId)
    if (filterByClientId != ""):
        query = query.filter(models.JobOrm.client_id == filterByClientId)
    if searchByOperatingUnit != "":
        query = query.filter(
            models.JobOrm.operating_unit.contains(searchByOperatingUnit))
    if orderByManagertName == "asc":
        query = query.order_by(asc(models.JobOrm.job_manager_name))
    elif orderByManagertName == "desc":
        query = query.order_by(desc(models.JobOrm.job_manager_name))
    query = query.offset(offset).limit(limit)

    size = query.count()

    return {
        "total": total,
        "size": size,
        "offset": offset,
        "limit": limit,
        "jobs": [schemas.Job.from_orm(job) for job in query.all()]
    }
