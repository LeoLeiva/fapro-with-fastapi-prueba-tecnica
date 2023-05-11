from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestCaseValidateDate:
    URL = "/uf/direct/%s/"

    def test_incorrect_date_format(self):
        date = "15-4-2022"
        response = client.get(self.URL % date)
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Incorrect date format. Use the format YYYY-MM-DD.",
        }

    def test_date_outside_range(self):
        date = "2010-4-22"
        response = client.get(self.URL % date)
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Date outside range",
        }

    def test_date_not_exist(self):
        date = "2022-2-30"
        response = client.get(self.URL % date)
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Incorrect date format. Use the format YYYY-MM-DD.",
        }
