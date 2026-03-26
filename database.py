"""This module uses SQLAlchemy to establish a database connection and session management for the application.
It loads the database URL from environment variables,
creates an engine, and defines a session factory and base class for declarative models."""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Provide a fallback for environments without a .env file (like GitHub Actions)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todoapp.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
