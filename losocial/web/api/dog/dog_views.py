from typing import Any, List

from fastapi import APIRouter, Depends

from losocial.db.dao.dog_dao import DogDAO
from losocial.db.models.users import current_active_user
from losocial.web.api.dog.request.dog_request import DogModelRequest
from losocial.web.api.dog.response.dog_response import DogModelResponse

router = APIRouter()


@router.get("/", response_model=List[DogModelResponse])
async def get_dogs(
    limit: int = 10,
    offset: int = 0,
    dog_dao: DogDAO = Depends(),
    user: Any = Depends(current_active_user),
) -> List[DogModelResponse]:
    return await dog_dao.get_all_dogs(limit, offset)  # type: ignore[return-value]


@router.post("/", response_model=DogModelResponse)
async def create_dog(
    request: DogModelRequest,
    dog_dao: DogDAO = Depends(),
    user: Any = Depends(current_active_user),
) -> DogModelResponse:
    return await dog_dao.create_dog_model(request)  # type: ignore[return-value]
