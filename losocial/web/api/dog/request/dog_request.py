from pydantic import BaseModel

from losocial.enums.dog_races import DogRacesEnum


class DogModelRequest(BaseModel):
    name: str
    owner_name: str
    age: int
    race: DogRacesEnum
