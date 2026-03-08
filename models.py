from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database import Base


class Users(Base):
    '''
    This class defines a SQLAlchemy model for a "User" table in a database.
    It inherits from the Base class, which is a declarative base provided by SQLAlchemy.
    '''
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # New column to store user roles (e.g., "admin", "user", etc.)


class Todos(Base):
    '''
    This class defines a SQLAlchemy model for a "Todos" table in a database.
    It inherits from the Base class, which is a declarative base provided by SQLAlchemy.
    '''
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
