from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import models
from database import session_local, engine
from models import Todos

app = FastAPI()
# This line creates all the tables defined in the models (in this case, the Todos table) in the database if they do not already exist. It uses the metadata from the Base class to generate the necessary SQL commands to create the tables based on the defined models.
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
     this function is a dependency that provides a database session for the duration of a request.
     It creates a new session using SessionLocal,
     yields it for use in the request,
     and ensures that the session is closed after the request is completed, even if an error occurs.
    """
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# This is a type annotation that indicates that the get_db
db_dependency = Annotated[Session, Depends(get_db)]


# function is a dependency that provides a Session object for database interactions.

@app.get("/", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency):
    """
    :param db: This parameter is a database session that is provided by the get_db dependency. It allows the function to interact with the database.
     The function uses this session to query the Todos table and retrieve all records, which are then returned as a response to the client.
    :return: The function returns a list of all records from the Todos table in the database.
     Each record is represented as an instance of the Todos model, which includes fields such as id, title, description, priority, and complete.
     The response will be a JSON array containing these records when the endpoint is accessed via a GET request to the root URL ("/").

    """
    return db.query(Todos).all()


@app.get("/todo/{id}", status_code=status.HTTP_200_OK)
def read_todo(db: db_dependency, id: int):
    """
    :param id: This parameter is an integer that represents the unique identifier of a specific todo item in the database. It is extracted from the URL path when a client makes a GET request to the "/todo/{id}" endpoint.
    :param db: This parameter is a database session provided by the get_db dependency, allowing the function to interact with the database.
     The function uses this session to query the Todos table and retrieve the record that matches the provided id, which is then returned as a response to the client.
    :return: The function returns a single record from the Todos table that matches the provided id. This record is represented as an instance of the Todos model, which includes fields such as id, title, description, priority, and complete.
     If a record with the specified id exists in the database, it will be returned as a JSON object when the endpoint is accessed via a GET request to "/todo/{id}". If no such record exists, it may return null or an appropriate error message depending on how you handle such cases in your application.

    """
    todo_model = db.query(Todos).filter(Todos.id == id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f'Todo with id {id} not found')
