from faker import Faker
from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import Field, SQLModel

fake = Faker()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str


# class UserCreate(BaseModel):
#     email: EmailStr
#     first_name: str
#     last_name: str
#     avatar: HttpUrl

class UserCreate(BaseModel):
    email: EmailStr = Field(default=fake.email())
    first_name: str = Field(default=fake.first_name())
    last_name: str = Field(default=fake.last_name())
    avatar: HttpUrl = Field(default=fake.url())


class UserCreateResponse(BaseModel):
    first_name: str
    avatar: HttpUrl
    last_name: str
    id: int
    email: EmailStr


class UserUpdate(BaseModel):
    email: EmailStr = Field(default=None)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    avatar: HttpUrl = Field(default=None)


class UserHeaders(BaseModel):
    accept: str = Field(default='application/json')
    content_type: str = Field(default='application/json')