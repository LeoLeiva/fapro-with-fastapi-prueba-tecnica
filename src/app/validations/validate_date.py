from datetime import datetime

from fastapi import HTTPException


def validate_date(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Incorrect date format. Use the format YYYY-MM-DD."
        )

    validate_date = datetime(
        year=int(date.split("-")[0]),
        month=int(date.split("-")[1]),
        day=int(date.split("-")[2]),
    ).date()

    if (
        validate_date < datetime(2013, 1, 1).date()
        or validate_date > datetime.now().date()
    ):
        raise HTTPException(status_code=400, detail="Date outside range")
