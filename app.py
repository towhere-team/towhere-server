from datetime import datetime, timedelta
from typing import List, Union

from fastapi import FastAPI
from humps import camelize
from pydantic import BaseModel

app = FastAPI()


def to_camel(str) -> str:
    return camelize(str)


class CamelCasedBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class TravelInfo(CamelCasedBaseModel):
    id: int
    departure_station: str
    departure_time: datetime
    destination_station: str
    destination_time: datetime
    cost: int
    time: timedelta


@app.get("/")
async def get_hello_world():
    return "Hello world!"


@app.get("/travel-infos/", response_model=List[TravelInfo])
async def search_travel_infos(
    dep: Union[str, None] = None,
    dest: Union[str, None] = None,
):
    if dep is None or dest is None:
        return []

    travel_info = TravelInfo(
        id=0,
        departure_station=dep,
        departure_time=datetime.now(),
        destination_station=dest,
        destination_time=datetime.now() + timedelta(minutes=60),
        cost=0,
        time=timedelta(minutes=60),
    )

    return [travel_info]
