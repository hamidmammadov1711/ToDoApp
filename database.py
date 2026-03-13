"""Bu modul, SQLAlchemy istifadə edərək tətbiq üçün verilənlər bazası bağlantısını və sessiya idarəetməsini qurur. Verilənlər bazası URL-ni mühit dəyişənlərindən yükləyir, mühərrik yaradır və deklarativ modellər üçün sessiya fabriki və baza sinfi təyin edir."""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
