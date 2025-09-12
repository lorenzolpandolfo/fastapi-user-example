from losocial.db.dao.dog_dao import DogDAO
from losocial.db.models.dog_model import DogModel
from losocial.enums.dog_age_stages import DogAgeStagesEnum
from losocial.web.api.dog.request.dog_request import DogModelRequest
from losocial.web.api.dog.response.dog_response import DogModelResponse

MAX_PUPPY_AGE = 1
MIN_JUNIOR_AGE = 2
MAX_JUNIOR_AGE = 3
MIN_ADULT_AGE = 4
MAX_ADULT_AGE = 7


class DogService:
    def __init__(self, dog_dao: DogDAO) -> None:
        self.dog_dao: DogDAO = dog_dao

    async def create_dog(self, request: DogModelRequest) -> DogModelResponse:
        dog_age_status: DogAgeStagesEnum

        if request.age <= MAX_PUPPY_AGE:
            dog_age_status = DogAgeStagesEnum.PUPPY
        elif request.age in (MIN_JUNIOR_AGE, MAX_JUNIOR_AGE):
            dog_age_status = DogAgeStagesEnum.JUNIOR
        elif MIN_ADULT_AGE <= request.age <= MAX_ADULT_AGE:
            dog_age_status = DogAgeStagesEnum.ADULT
        else:
            dog_age_status = DogAgeStagesEnum.SENIOR

        dog = DogModel(**request.model_dump())
        dog.age_stage = dog_age_status

        return await self.dog_dao.save(dog)  # type: ignore
