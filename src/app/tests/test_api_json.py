from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestCaseJsonAPI:
    URL = "/uf/json/%s/"

    def test_get_value_200_ok_from_json(self):
        date = "2022-6-15"
        response = client.get(self.URL % date)
        assert response.status_code == 200
        assert response.json() == {
            "date": date,
            "value": "32.890,08"
        }
