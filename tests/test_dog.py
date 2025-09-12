import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from losocial.db.dao.dog_dao import DogDAO
from losocial.db.models.dog_model import DogModel
from losocial.enums.dog_age_stages import DogAgeStagesEnum
from losocial.enums.dog_races import DogRacesEnum
from losocial.web.api.dog.request.dog_request import DogModelRequest
from tests.conftest import (
    register_and_login_default_user,
    save_and_expect,
)


def create_dog(
    name: str = "Rex",
    age: int = 5,
    race: DogRacesEnum = DogRacesEnum.SHIH_TZU,
    owner_name: str = "Lorenzo",
) -> DogModel:
    return DogModel(
        name=name,
        age=age,
        owner_name=owner_name,
        race=race,
        age_stage=DogAgeStagesEnum.PUPPY,
    )


@pytest.mark.anyio
async def test_create_dog(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests dog instance creation."""

    name = "dog"
    age = 10
    owner_name = "Lorenzo"
    race = DogRacesEnum.POODLE
    url = fastapi_app.url_path_for("create_dog")

    token = await register_and_login_default_user(client)

    request = DogModelRequest(
        name=name,
        age=age,
        owner_name=owner_name,
        race=race,
    )

    response: Response = await client.post(
        url,
        json=request.model_dump(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.anyio
async def test_create_dog_must_error_when_not_auth(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests dog instance creation."""

    name = "dog"
    age = 10
    owner_name = "Lorenzo"
    race = DogRacesEnum.POODLE
    url = fastapi_app.url_path_for("create_dog")

    request = DogModelRequest(
        name=name,
        age=age,
        owner_name=owner_name,
        race=race,
    )

    response: Response = await client.post(
        url,
        json=request.model_dump(),
        headers={"Authorization": f"Bearer mytoken"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_get_dog(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests dog instance creation."""
    name = "dog"

    url = fastapi_app.url_path_for("get_dogs")
    dog_dao = DogDAO(dbsession)

    token = await register_and_login_default_user(client)

    dog = create_dog(name=name)

    await save_and_expect(dog_dao, dog, 1)

    response: Response = await client.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body[0]["id"]
    assert body[0]["name"] == name


@pytest.mark.anyio
async def test_get_dog_must_error_when_not_auth(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests dog instance creation."""
    url = fastapi_app.url_path_for("get_dogs")
    dog_dao = DogDAO(dbsession)

    dog = create_dog()

    await save_and_expect(dog_dao, dog, 1)

    response: Response = await client.get(
        url,
        headers={"Authorization": f"Bearer token"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
