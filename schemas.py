from pydantic import BaseModel, EmailStr
from datetime import date, datetime

class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    contact: str
    password: str

class UserBasicInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    contact: str
    email: EmailStr
    ac_creation: date
    is_admin: bool


class OTPBody(BaseModel):
    email: EmailStr
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str
    is_admin: bool


class RentRequestBody(BaseModel):
    title: str
    description: str
    location: str
    price: float

class UserInfoForAd(BaseModel):
    id: int
    first_name: str
    contact: str
    email: EmailStr


class AdResponseSchema(RentRequestBody):
    id: int
    user: UserInfoForAd