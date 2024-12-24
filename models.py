from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from datetime import date, datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, index=True, default=None)
    first_name: str
    last_name: str | None
    email: EmailStr = Field(unique=True, index=True)
    contact: str = Field(unique=True)
    password: str
    is_active: bool | None = Field(default=False)
    is_admin: bool | None = Field(default=False)
    ac_creation: date = Field(default=None)
    ac_updation: date | None = Field(default=None)

    rents: list["Rents"] = Relationship(back_populates="user")

class Rents(SQLModel, table=True):
    __tablename__ = 'rents'

    id: int = Field(primary_key=True, index=True, default=None)
    user_id: int = Field(foreign_key="users.id")
    title: str
    description: str
    location: str
    price: float
    created_at: datetime | None = Field(default= datetime.now())
    user: User = Relationship(back_populates='rents')