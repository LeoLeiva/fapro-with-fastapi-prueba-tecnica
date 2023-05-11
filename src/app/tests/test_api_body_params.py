from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestCaseAPIBodyParams:
    URL = "/uf/"

    def test_get_value_ok_with_body_params(self):
        date = "2021-4-2"
        data = {
            'date': date,
            'method': 'json'
        }
        response = client.post(self.URL, json=data)
        assert response.status_code == 200
        assert response.json() == {
            'date': '2021-4-2',
            'value': '29.398,56',
            'method': 'json'
        }
