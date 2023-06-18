FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./job_schedule_app /code/job_schedule_app
COPY ./planning.json /code/planning.json

CMD ["uvicorn", "job_schedule_app.main:app", "--host", "0.0.0.0", "--port", "80"]