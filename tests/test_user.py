import pytest
from fastapi import FastAPI
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tests.conftest import register_and_login_default_user, register_user


@pytest.mark.anyio
async def test_register_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    email = "foo@mail.com"
    password = "pass123"
    teste = "123"

    response: Response = await client.post(
        "/api/auth/register",
        json={"email": email, "password": password, "teste": teste},
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["email"] == email
    assert "id" in body


@pytest.mark.anyio
async def test_login_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    email = "foo@mail.com"
    password = "pass123"
    teste = ""

    await register_user(client, email, password, teste)

    response: Response = await client.post(
        "/api/auth/jwt/login",
        data={"username": email, "password": password},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

    return body["access_token"]


@pytest.mark.anyio
async def test_authenticated_request(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    email = "mock@mail.com"

    token = await register_and_login_default_user(client)

    response: Response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["email"] == email
    assert "id" in body


@pytest.mark.anyio
async def test_authenticated_request_must_error_when_not_auth(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    email = "mock@mail.com"

    response: Response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer token123"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
