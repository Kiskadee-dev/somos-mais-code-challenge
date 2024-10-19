from pydantic import (
    AfterValidator,
    BaseModel,
    EmailStr,
    HttpUrl,
    Field,
    BeforeValidator,
    ValidationError,
)
from typing import Annotated, Literal, Optional
from decimal import Decimal
from datetime import datetime

from ApiClientes.api_clientes.clients.client.phone_conversion import convert_br_to_e164
import re


class UserName(BaseModel):
    title: str
    first: str
    last: str


class UserCoordinates(BaseModel):
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class UserTimezone(BaseModel):
    def validate_offset(offset: str) -> None:
        pattern = r"0{1,2}:0{2}"
        has_match = re.match(pattern, offset)
        if has_match is not None:
            return

        pattern = r"[-+]\d{1,2}:\d{2}"
        has_match = re.match(pattern, offset)
        if has_match is None:
            raise ValidationError(f"Invalid timezone offset {offset}")

        pattern = r"[-+](\d{1,2}):(\d{2})"
        times = re.findall(pattern, offset)
        assert len(times) == 1
        hour, minutes = times[0]
        hour = int(hour)
        minutes = int(minutes)
        assert hour >= 0 and hour <= 23
        assert minutes >= 0 and minutes < 60

    offset: Annotated[str, AfterValidator(validate_offset)]
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
    def migrate_gender(gender: str) -> str:
        """
        Migrates a gender string to its corresponding code as defined by ISO/IEC 5218:
        - M = Male;
        - F = Female;
        - O = Other (for non-binary, unknown, or unspecified genders).

        Currently, the system uses 'M', 'F', and 'O' for gender representation.
        However, ISO/IEC 5218 defines a standard for gender encoding that might be
        considered for future improvements.

        Args:
            gender (str): gender to be migrated

        Returns:
            str: Char representing the gender
        """
        if len(gender) == 1:
            return gender
        match gender.lower():
            case "male":
                return "M"
            case "female":
                return "F"
            case _:
                return "O"

    gender: Annotated[str, BeforeValidator(migrate_gender), Literal["M", "F", "O"]]
    name: UserName
    location: UserLocation

    def sanitize_email(email: str) -> str:
        """
        The given dataset doesn't seem to provide properly sanitized emails
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
