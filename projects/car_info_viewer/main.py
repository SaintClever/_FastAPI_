from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Car(BaseModel):
    make: str
    model: str
    year: int = Field(..., ge=1970, lt=2022)
    price: float
    engine: Optional[str] = "V4"
    autonomous: bool
    sold: List[str]


app = FastAPI()

@app.get("/")
def root():
    return {"Welcome to": "Your first API in FastAPI"}


@app.get("/cars", response_model=List[Dict[str, Car]])
def get_cars():
