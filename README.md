# Backend Coding Challenge

At aspaara a squad of superheroes works on giving superpowers to planning teams.
Through our product dashboard, we give insights into data – a true super-vision
superpower. Join forces with us and build a dashboard of the future!

![aspaara superhero](aspaara_superhero.png)

## Goal

Create a simple backend application that provides an API for a dashboard which
allows a planner to get insights into client and planning information.

You will find the corresponding data that needs to be imported into the database
in `planning.json`, which contains around 10k records.

## Requirements

1. Create proper database tables that can fit the data model.
2. Create a script that imports the data into the database (sqlite).
3. Create REST APIs to get the planning data from the database.
    1. The APIs don't need to be complete, just create what you can in the
       available time.
    2. Please include at least one example on how to do each of the following:
        1. pagination
        2. sorting
        3. filtering / searching

## Solution
- The data-set is denormalized. Hence the first step is to normalize the data, and import into the sqlite3 database. (Article explaining normalization and normal forms: https://www.javatpoint.com/dbms-normalization). The import function is in `job_schedule_app/init_db.py`.
- Models are: Talent, Skill, Office, Client and Job
- Pagination, sorting, filtering & searching examples are found in the generated docs: After starting the applications with the steps below, visit `http://localhost:8000/docs`
- Corresponding tests are found in `job_schedule_app/api_test.py`

### How to Run the Application
- Ensure you have docker installed. From the root directory, run: `docker build -t scheduler .`  
- This builds the docker image and tags it as "scheduler".
- Next, run: `docker run -d --name mycontainer -p 8000:80 scheduler`
- This starts a docker container and names it "mycontainer" (the name will be used to run tests).
- Visit: `http://localhost:8000/docs`

### How to Import the planning.json Data into the DB
- Simply visit: `http://localhost:8000/initDatabase`
- It should take less than 30 seconds to import all 10k items.
- Alternatively, execute it within the docs page.

### How to Run Tests
- While the app is running (steps above), run `docker exec mycontainer pytest -v`

## Data Model

* ID: integer (unique, required)
* Original ID: string (unique, required)
* Talent ID: string (optional)
* Talent Name: string (optional)
* Talent Grade: string (optional)
* Booking Grade: string (optional)
* Operating Unit: string (required)
* Office City: string (optional)
* Office Postal Code: string (required)
* Job Manager Name: string (optional)
* Job Manager ID: string (optional)
* Total Hours: float (required)
* Start Date: datetime (required)
* End Date: datetime (required)
* Client Name: string (optional)
* Client ID: string (required)
* Industry: string (optional)
* Required Skills: array of key-value pair (optional)
* Optional Skills: array of key-value pair (optional)
* Is Unassigned: boolean

## Preferred Tech Stack

* Python 3.8+
* FastAPI
* SQLAlchemy

## Submission

* Please fork the project, commit and push your implementation and then send us
  the link to your fork.
* Please update the README with any additional details or steps that are
  required to run your implementation.
* We understand that there is a limited amount of time, so it does not have to
  be perfect or 100% finished. Plan to spend no more than 2-3 hours on it.

For any additional questions on the task please feel free to email us!
