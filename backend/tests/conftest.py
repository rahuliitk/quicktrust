import asyncio
import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base
from app.core.dependencies import get_db, get_current_user
from app.main import app
from app.models.user import User

# Use a separate test database or SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with test_session() as session:
        yield session


def make_test_user() -> User:
    return User(
        id=uuid.uuid4(),
        org_id=uuid.uuid4(),
        keycloak_id="test-keycloak-id",
        email="test@quicktrust.dev",
        full_name="Test User",
        role="super_admin",
        is_active=True,
    )


async def override_get_current_user():
    return make_test_user()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def db():
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture
async def test_org(client):
    resp = await client.post("/api/v1/organizations", json={"name": "Test Org", "slug": "test-org-shared"})
    return resp.json()["id"]


def make_test_user_with_role(role: str) -> User:
    return User(
        id=uuid.uuid4(),
        org_id=uuid.uuid4(),
        keycloak_id=f"test-{role}-id",
        email=f"{role}@quicktrust.dev",
        full_name=f"Test {role.title()}",
        role=role,
        is_active=True,
    )
