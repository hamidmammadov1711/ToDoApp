from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class Todos(Base):
    '''
    This class defines a SQLAlchemy model for a "Todos" table in a database.
    It inherits from the Base class, which is a declarative base provided by SQLAlchemy.
    '''
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True) # Integer column that serves as the primary key for the table, with an index for faster lookups.
    title = Column(String) # VARCHAR in SQL, used to store text data.
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False) # Boolean column that indicates whether a todo item is complete, with a default value of False.



