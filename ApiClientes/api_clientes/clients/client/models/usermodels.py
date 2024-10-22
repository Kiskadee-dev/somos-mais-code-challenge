from pydantic import (
    BaseModel,
    EmailStr,
    HttpUrl,
    Field,
    BeforeValidator,
    ValidationError,
    computed_field,
)
from typing import Annotated, Literal
from decimal import Decimal
from datetime import datetime

from api_clientes.clients.regions.definitions.locations import find_region
from api_clientes.clients.client.phone_conversion import convert_br_to_e164
from api_clientes.clients.regions.tags import Tag
import re


class UserName(BaseModel):
    title: str
    first: str
    last: str


class UserCoordinates(BaseModel):
    latitude: Decimal
    longitude: Decimal


class UserTimezone(BaseModel):
    def validate_offset(offset: str) -> None:
        assert type(offset) is str

        pattern = r"0{1,2}:0{2}"
        has_match = re.match(pattern, offset)
        if has_match is not None:
            return offset

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
        assert (hour >= 0 and hour <= 23) or (hour <= 0 and hour >= -23)
        assert minutes >= 0 and minutes < 60
        return offset

    offset: Annotated[str, BeforeValidator(validate_offset)]
    description: str


class UserLocation(BaseModel):
    @computed_field
    @property
    def region(self) -> str:
        region = find_region(self.state)
        assert region is not None
        return region.value

    street: str
    city: str
    state: str
    postcode: int
    coordinates: UserCoordinates
    timezone: UserTimezone


class UserPicture(BaseModel):
    def validate(url) -> str:
        valid_url = HttpUrl(url)
        return str(valid_url)

    large: Annotated[str, BeforeValidator(validate)]
    medium: Annotated[str, BeforeValidator(validate)]
    thumbnail: Annotated[str, BeforeValidator(validate)]


class UserModel(BaseModel):
    @computed_field
    @property
    def type(self) -> str:
        return Tag.get_tag(
            self.location.coordinates.longitude, self.location.coordinates.latitude
        ).value

    def migrate_gender(gender: str) -> str:
        """
        Migrates a gender string to its corresponding code:
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

    def migrate_dates(date: str | dict):
        if type(date) is str:
            return date
        assert "date" in date
        return date["date"]

    birthday: Annotated[datetime, BeforeValidator(migrate_dates), Field(alias="dob")]
    registered: Annotated[datetime, BeforeValidator(migrate_dates)]

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
    nationality: str = "BR"
