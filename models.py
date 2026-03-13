"""Bu modul verilənlər bazasındakı "User" və "Todo" cədvəlləri üçün SQLAlchemy modellərini müəyyən edir. "Users" sinfi istifadəçi adı, e-poçt, ad, soyad, heş edilmiş parol, aktiv status və rol kimi istifadəçi məlumatları üçün sahələri özündə birləşdirən "users" cədvəlinin strukturunu təmsil edir. "Todos" sinfi başlıq, təsvir, prioritet, tamamlanma statusu və todo sahibinə (istifadəçiyə) keçid verən xarici açar kimi todo məlumatları üçün sahələri özündə birləşdirən "todos" cədvəlinin strukturunu təmsil edir. Hər iki sinif SQLAlchemy-nin deklarativ sistemi tərəfindən təmin edilən Base sinifindən miras qalır. """
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)  # New column to store user roles (e.g., "admin", "user", etc.)


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
