import requests


def test_get_item():
    url = "https://qa-internship.avito.com/api/1/item/0cd4183f-65f5-4f00-a27c-ee6b7d379a55"
    response = requests.get(url)

    assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"

    data = response.json()
    assert "result" in data
    assert data["status"] == "404"
    print("Тест пройден")


if __name__ == "__main__":
    test_get_item()
