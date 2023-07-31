import pytest

from src.menu.schemas import MenuCreate


class TestCreateMenu:

    @pytest.mark.anyio
    async def test_get_menus(self, ac, db_with_menus):
        response = await ac.get("/api/v1/menus/")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["title"] == "Test menu 1"
        assert response.json()[1]["description"] == "Test menu description 2"

    @pytest.mark.anyio
    async def test_create_menu(self, ac):
        new_menu = MenuCreate(
            title="My menu 1",
            description="My menu description 1"
        )
        response = await ac.post("/api/v1/menus/", json=new_menu.model_dump())
        assert response.status_code == 201
        assert response.json()["title"] == "My menu 1"
        assert response.json()["description"] == "My menu 1"
