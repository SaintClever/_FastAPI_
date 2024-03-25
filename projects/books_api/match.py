from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class Gender(Enum):
    male = "male"
    female = "female"


class Match:
    id: int
    name: str
    age: int
    gender: str

    def __init__(self, id, name, age, gender):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender


class MatchRequest(BaseModel):
    id: int | None = Field(description="ID not needed", default=None)
    name: str = Field(min_length=2, max_length=15)
    age: int = Field(gt=15, lt=100)
    gender: Gender

    class Config:
        json_schema_extra = {
            "example": {"id": 100, "name": "Eve", "age": 25, "gender": Gender.female}
        }


MATCHES = [
    Match(1, "Nesta", 4, Gender.male),
    Match(2, "Parchment", 40, Gender.male),
    Match(3, "Saint. Clever", 30, Gender.male),
]


# http://127.0.0.1:8000/matches
@app.get("/matches")
async def get_matches():
    return MATCHES


# http://127.0.0.1:8000/match/{id}?match_id=1
@app.get("/match/{id}")
async def get_match(match_id: int):
    for match in MATCHES:
        if match_id == match.id:
            return match


@app.post("/match/")
async def post_match(match: MatchRequest):
    new_match = Match(**match.model_dump())
    MATCHES.append(new_match)


@app.put("/match/update_match")
async def put_match(match: MatchRequest):
    for i in range(len(MATCHES)):  # Loop thru the length matches
        if MATCHES[i].id == match.id:  # if the query id is equal to the MATCHES id
            # Take that specific match and update it with match: MatchRequest
            MATCHES[i] = match


@app.delete("/match/delete_match")
async def delete_match(match_id: int):
    for i in range(len(MATCHES)):
        if MATCHES[i].id == match_id:
            MATCHES.pop(i)  # pop takes an index
            break
