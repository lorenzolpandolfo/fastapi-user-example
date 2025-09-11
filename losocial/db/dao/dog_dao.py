from typing import Any, Coroutine, List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from losocial.db.dependencies import get_db_session
from losocial.db.models.dog_model import DogModel
from losocial.web.api.dog.request.dog_request import DogModelRequest


class DogDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def get_all_dogs(self, limit: int, offset: int) -> List[DogModel]:

        raw_dogs = await self.session.execute(
            select(DogModel).limit(limit).offset(offset),
        )
        return list(raw_dogs.scalars().fetchall())

    async def create_dog_model(self, request: DogModelRequest) -> DogModel:
        dog = DogModel(**request.model_dump())
        self.session.add(dog)
        await self.session.flush()
        return dog

