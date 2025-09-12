from typing import Annotated, Any, List

from fastapi import APIRouter, Depends

from losocial.db.dao.dog_dao import DogDAO
from losocial.db.models.users import current_active_user
from losocial.services.dog_service import DogService
from losocial.web.api.dog.request.dog_request import DogModelRequest
from losocial.web.api.dog.response.dog_response import DogModelResponse

router = APIRouter()


def get_dog_service(dog_dao: Annotated[DogDAO, Depends()]) -> DogService:
    return DogService(dog_dao=dog_dao)


@router.get("/", response_model=List[DogModelResponse])
async def get_dogs(
    user: Annotated[Any, Depends(current_active_user)],
    limit: int = 10,
    offset: int = 0,
    dog_dao: DogDAO = Depends(),
) -> List[DogModelResponse]:
    return await dog_dao.get_all_dogs(limit, offset)  # type: ignore[return-value]


@router.post("/", response_model=DogModelResponse)
async def create_dog(
    request: DogModelRequest,
    service: Annotated[DogService, Depends(get_dog_service)],
    user: Annotated[Any, Depends(current_active_user)],
) -> DogModelResponse:
    return await service.create_dog(request)
