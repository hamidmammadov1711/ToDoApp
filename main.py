from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette import status

import models
from database import SessionLocal, engine
from models import Todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    """
     this function is a dependency that provides a database session for the duration of a request.
     It creates a new session using SessionLocal,
     yields it for use in the request,
     and ensures that the session is closed after the request is completed, even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)] # This is a type annotation that indicates that the get_db
# function is a dependency that provides a Session object for database interactions.

@app.get("/", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency):
    """
    :param db: This parameter is a database session that is provided by the get_db dependency. It allows the function to interact with the database.
     The function uses this session to query the Todos table and retrieve all records, which are then returned as a response to the client.
    :return: The function returns a list of all records from the Todos table in the database. Each record is represented as an instance of the Todos model, which includes fields such as id, title, description, priority, and complete. The response will be a JSON array containing these records when the endpoint is accessed via a GET request to the root URL ("/").

    """
    return db.query(Todos).all()

