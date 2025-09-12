import uuid

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from losocial.db.base import Base
from losocial.enums.dog_age_stages import DogAgeStagesEnum
from losocial.enums.dog_races import DogRacesEnum


class DogModel(Base):

    __tablename__ = "dog"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(length=200))
    owner_name: Mapped[str] = mapped_column(String(length=200))
    age: Mapped[int] = mapped_column(Integer)
    age_stage: Mapped[DogAgeStagesEnum] = mapped_column(Enum(DogAgeStagesEnum))
    race: Mapped[DogRacesEnum] = mapped_column(Enum(DogRacesEnum))
