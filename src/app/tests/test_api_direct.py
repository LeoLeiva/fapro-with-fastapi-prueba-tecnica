from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestCaseDirectAPI:
    URL = "/uf/direct/%s/"

    def test_get_value_200_ok_from_endpoint(self):
        date = "2022-4-5"
        response = client.get(self.URL % date)
        assert response.status_code == 200
        assert response.json() == {
            "date": date,
            "value": "31.743,07"
        }
