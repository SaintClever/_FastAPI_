from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from projects.car_info_viewer.database import cars


class Car(BaseModel):
  make: str
  model: str
  year: int = Field(..., get=1970, lt=2022)
  price: float
  engine: Optional[str] = "V4"
  autonomous: bool
  sold: List[str]


app = FastAPI()


@app.get("/")
def root():
  return {"Hello": "World!"}


@app.get("/cars", response_model=List[Dict[str, Car]])
def get_cars(number: Optional[str] = Query(...)):
  return ...