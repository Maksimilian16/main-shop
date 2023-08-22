from pydantic import BaseModel, EmailStr, constr
from settings import Base
from sqlalchemy import Column, Integer, String, JSON
from settings import Base


class UsersTable(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    login = Column(String)
    password = Column(String)
    basket = Column(JSON)


class Products(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    owner = Column(String)
    description = Column(String)


class LoginPage(BaseModel):
    login: str
    password: str


class RegistrationPage(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=50)
    login: constr(min_length=3, max_length=20)
    password_confirmation: str


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str | None


class Filters(BaseModel):
    min: float
    max: float
    name: str
