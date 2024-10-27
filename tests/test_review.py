import pytest
from services.github_service import *
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_analyze_code_success():
    request_data = {
        "description": "Analyze code",
        "github_repo_url": "https://github.com/froozy3/CodeReviewAI",
        "candidate_level": "Junior"
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/analyze-code", json=request_data)

    assert response.status_code == 200, {f"Expected status code 200, got {response.status_code}"}
    data = response.json()
    assert 'found_files' in data
    assert 'downsides' in data
    assert 'rating' in data
    assert 'conclusion' in data


@pytest.mark.asyncio
async def test_analyze_code_error():
    request_data = {
        "description": "Analyze code",
        "github_repo_url": "invalid-url",
        "candidate_level": "junior"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/analyze-code", json=request_data)

        assert response.status_code == 200
