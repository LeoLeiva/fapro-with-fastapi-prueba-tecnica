import calendar
import json
import locale
from datetime import datetime, timedelta

import requests
import uvicorn
from bs4 import BeautifulSoup
from fastapi import Body, FastAPI, HTTPException
from fastapi_utils.tasks import repeat_every
from app.validations.validate_date import validate_date

app = FastAPI()


# We configure the local language in Spanish for the search of the month
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


@app.get("/uf/direct/{date}")
def get_uf_direct_value(date: str):
    """
    Method that returns the UF value based on the date sent in the
    endpoint url and tracked directly from the values ​​site
    """
    validate_date(date)
    url = f"https://www.sii.cl/valores_y_fechas/uf/uf{date[:4]}.htm"
    response = requests.get(url)
    if response.status_code == 200:
        uf_value = parse_uf_value(response.text, date)
        if uf_value is not None:
            return {"date": date, "value": uf_value}
    raise HTTPException(status_code=404, detail="UF value not found")


@app.get("/uf/json/{date}/")
def get_uf_json_value(date: str):
    """
    Method that returns the UF value based on the date sent in the
    endpoint url and tracked from a json that is updated periodically
    """
    validate_date(date)
    get_data = open('app/data/valores_uf.json')
    data = json.load(get_data)

    year = date.split("-")[0]
    number_month = date.split("-")[1]
    str_month = calendar.month_name[int(number_month)]
    day = date.split("-")[2]
    uf_value = data[year][str_month].get(day)
    if uf_value:
        return {"date": date, "value": uf_value}
    raise HTTPException(status_code=404, detail="UF value not found")


@app.post('/uf/')
def get_uf_with_body_params(date: str = Body(...), method: str = Body(...)):
    """
    Method that returns the UF value based on the date sent in the endpoint url
    and tracked directly from the values ​​site

    example body:
    {
        'date': '2022-4-5,
        'method': 'json'
    }
    """
    if method == "direct":
        value = get_uf_direct_value(date)
    elif method == "json":
        value = get_uf_json_value(date)
    else:
        raise HTTPException(status_code=400, detail="error: method incorrect")
    value.update({"method": method})
    return value


def parse_uf_value(html: str, date: str):
    """
    Passing the html code and the date str('2022-3-4'), it returns a json with the value of UF on that date
    """
    value = None
    soup = BeautifulSoup(html, "html.parser")

    number_month = date.split("-")[1]
    str_month = f"mes_{calendar.month_name[int(number_month)]}"
    element = soup.find("div", {"id": str_month})
    table = element.find("table")
    rows = table.find_all("tr")
    for row in rows:
        data = row.find_all("th", string=date.split("-")[2])
        if data:
            value = data[0].find_next("td").text
            break

    return value


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # 24 hours
def update_json_value_uf():
    """
    Task to periodically update the json with the UF values. Just search the last 3 days from today.
    The variable days_back indicates the number of days backwards.
    """
    days_back = 3
    end_date = datetime.now().date() + timedelta(days=1)
    start_date = end_date - timedelta(days=days_back)
    dates = [(start_date + timedelta(n)) for n in range(int((end_date - start_date).days))]

    get_data = open('app/data/valores_uf.json')
    data = json.load(get_data)
    old_data = data
    for date in dates:
        str_date = date.strftime("%Y-%-m-%-d")
        str_month = calendar.month_name[int(date.month)]

        # If keys do not exist, it is create
        if not str(date.year) in data:
            data[str(date.year)] = {}
        if not str_month in data[str(date.year)]:
            data[str(date.year)][str_month] = {}

        # Check if value exist in json, if not exist add value
        if not str(date.day) in data[str(date.year)][str_month]:
            json_value = get_uf_direct_value(date=str_date)
            if not json_value.get("value"):
                raise HTTPException(status_code=400, detail="Bad request")
            value = json_value.get("value")

            data[str(date.year)][str_month][str(date.day)] = value


    # Save JSON with new value
    if not old_data != data:
        with open('app/data/valores_uf.json', 'w+') as file:
            json.dump(data, file, indent=4, sort_keys=True)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
