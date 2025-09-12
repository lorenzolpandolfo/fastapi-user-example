from uuid import UUID

from pydantic import BaseModel, ConfigDict

from losocial.enums.dog_age_stages import DogAgeStagesEnum


class DogModelResponse(BaseModel):
    id: UUID
    name: str
    age_stage: DogAgeStagesEnum

    model_config = ConfigDict(from_attributes=True)
