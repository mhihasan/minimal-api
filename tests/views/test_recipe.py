from src.models.recipe import Recipe


def test_list_recipes(client):
    Recipe(name="test", difficulty=1, prep_time=10).save()
    response = client.get("/recipes/")
    assert len(response.json) == 1
    assert response.status_code == 200
