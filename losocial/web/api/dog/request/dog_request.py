from pydantic import BaseModel, field_validator

from losocial.enums.dog_races import DogRacesEnum


class DogModelRequest(BaseModel):
    name: str
    owner_name: str
    age: int
    race: DogRacesEnum

    @field_validator("age")
    def validate_age(cls, age: int) -> int:  # noqa: N805
        if age <= 0:
            raise ValueError("age must be greater than zero")
        return age
