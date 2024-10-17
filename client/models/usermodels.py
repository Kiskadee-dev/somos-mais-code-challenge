from pydantic import BaseModel, EmailStr, HttpUrl
from decimal import Decimal
from datetime import datetime


class UserName(BaseModel):
    title: str
    first: str
    last: str


class UserCoordinates(BaseModel):
    latitude: Decimal
    longitude: Decimal


class UserLocation(BaseModel):
    street: str
    city: str
    state: str
    postcode: int
    coordinates: UserCoordinates


class UserTimezone(BaseModel):
    offset: str  # TODO: validate
    description: str


class UserDateOfBirth(BaseModel):
    date: datetime


class UserRegistered(BaseModel):
    date: datetime


class UserPicture(BaseModel):
    large: HttpUrl
    medium: HttpUrl
    thumbnail: HttpUrl


class UserModel(BaseModel):
    gender: str
    name: UserName
    location: UserCoordinates
    timezone: UserTimezone
    email: EmailStr
    dob: UserDateOfBirth
    registered: UserRegistered
    telephoneNumbers: list  # TODO: convert to E.164
    mobileNumbers: list  # TODO: convert to E.164
    picture: UserPicture
