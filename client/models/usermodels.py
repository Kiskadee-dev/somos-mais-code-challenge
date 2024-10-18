from pydantic import BaseModel, EmailStr, HttpUrl, Field, BeforeValidator
from typing import Annotated, Optional
from decimal import Decimal
from datetime import datetime
from client.phone_conversion import convert_br_to_e164
import re


class UserName(BaseModel):
    title: str
    first: str
    last: str


class UserCoordinates(BaseModel):
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class UserTimezone(BaseModel):
    offset: str  # TODO: validate
    description: str


class UserLocation(BaseModel):
    street: str
    city: str
    state: str
    postcode: int
    coordinates: UserCoordinates
    timezone: UserTimezone


class UserDateOfBirth(BaseModel):
    date: datetime


class UserRegistered(BaseModel):
    date: datetime


class UserPicture(BaseModel):
    large: HttpUrl
    medium: HttpUrl
    thumbnail: HttpUrl


class UserModel(BaseModel):
    gender: str  # TODO: Migrate to M or F
    name: UserName
    location: UserLocation

    def sanitize_email(email: str) -> str:
        """The given dataset doesn't seem to provide properly sanitized emails
        This replaces any space or chain of spaces into a dot
        Eg: Use r@example.com becomes Use.r@example.com
        Eg2: Use .r@example.com becomes Use.r@example.com

        Args:
            email (str)

        Returns:
            str: sanitized email
        """
        assert "@" in email
        name, domain = email.split("@")
        sanitized_name: str = re.sub(r"\s.?\s*", ".", name)
        return f"{sanitized_name}@{domain}"

    email: Annotated[EmailStr, BeforeValidator(sanitize_email)]
    dob: UserDateOfBirth
    registered: UserRegistered

    def migrate_phone_format(phone: list[str] | str) -> list[str]:
        if type(phone) is str:
            return [convert_br_to_e164(phone)]
        return phone

    telephoneNumbers: Annotated[
        list[str], Field(alias="phone"), BeforeValidator(migrate_phone_format)
    ]
    mobileNumbers: Annotated[
        list[str], Field(alias="cell"), BeforeValidator(migrate_phone_format)
    ]
    picture: UserPicture
