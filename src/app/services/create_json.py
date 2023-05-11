import calendar
import json
import locale
from datetime import datetime

import requests
from bs4 import BeautifulSoup


def create_json(year: str):
    url = f"https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    value_uf = {}
    # We configure the local language in Spanish for the search of the month
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
    all_month = list(calendar.month_name[1:])
    for month in all_month:
        str_month = f'mes_{month}'
        element = soup.find("div", {"id": str_month})

        if not element:
            continue
        table = element.find("table")
        rows = table.find_all("tr")
        for row in rows:
            columns = row.find_all("th")
            if columns[0].text == month.capitalize():
                continue

            for column in columns:
                if year not in value_uf:
                    value_uf[year] = {}
                if month not in value_uf[year]:
                    value_uf[year][month] = {}
                if column.find_next("td").text:
                    value_uf[year][month][column.text] = column.find_next("td").text
    return value_uf

value_uf = {}
for year in range(2013, datetime.now().year+1):
    values = create_json(str(year))
    value_uf.update(values)

with open("valores_uf.json", "w") as json_file:
    json.dump(value_uf, json_file, indent=4, sort_keys=True)
