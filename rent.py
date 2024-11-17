from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

# House model
class House:
    id: int
    name: str
    owner: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, name, owner, description, rating, published_date):
        self.id = id
        self.name = name
        self.owner = owner
        self.description = description
        self.rating = rating
        self.published_date = published_date


# House Request model
class HouseRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on creation", default=None)
    name: str = Field(min_length=3)
    owner: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sunny Villa",
                "owner": "John Doe",
                "description": "A beautiful villa with a sunny view.",
                "rating": 5,
                "published_date": 2029,
            }
        }
    }


# Initial list of houses
HOUSES = [
    House(1, "Sunny Villa", "John Doe", "A beautiful villa with a sunny view.", 5, 2030),
    House(2, "Cozy Apartment", "Jane Smith", "A cozy apartment in the city center.", 4, 2029),
    House(3, "Luxury Penthouse", "Sam Wilson", "A luxurious penthouse with modern amenities.", 5, 2028),
    House(4, "Budget Studio", "Alex Brown", "An affordable studio for rent.", 3, 2027),
    House(5, "Beach House", "Chris Green", "A house near the beach with scenic views.", 4, 2026),
    House(6, "Mountain Retreat", "Taylor White", "A retreat in the mountains.", 2, 2025),
]

# Endpoints
@app.get("/houses", status_code=status.HTTP_200_OK)
async def read_all_houses():
    return HOUSES


@app.get("/houses/{house_id}", status_code=status.HTTP_200_OK)
async def read_house(house_id: int = Path(gt=0)):
    for house in HOUSES:
        if house.id == house_id:
            return house
    raise HTTPException(status_code=404, detail="House not found")


@app.get("/houses/", status_code=status.HTTP_200_OK)
async def read_houses_by_rating(house_rating: int = Query(gt=0, lt=6)):
    houses_to_return = []
    for house in HOUSES:
        if house.rating == house_rating:
            houses_to_return.append(house)
    return houses_to_return


@app.get("/houses/publish/", status_code=status.HTTP_200_OK)
async def read_houses_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    houses_to_return = []
    for house in HOUSES:
        if house.published_date == published_date:
            houses_to_return.append(house)
    return houses_to_return


@app.post("/create-house", status_code=status.HTTP_201_CREATED)
async def create_house(house_request: HouseRequest):
    new_house = House(**house_request.model_dump())
    HOUSES.append(find_house_id(new_house))


def find_house_id(house: House):
    house.id = 1 if len(HOUSES) == 0 else HOUSES[-1].id + 1
    return house


@app.put("/houses/update_house", status_code=status.HTTP_204_NO_CONTENT)
async def update_house(house: HouseRequest):
    house_changed = False
    for i in range(len(HOUSES)):
        if HOUSES[i].id == house.id:
            HOUSES[i] = house
            house_changed = True
    if not house_changed:
        raise HTTPException(status_code=404, detail="House not found")


@app.delete("/houses/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_house(house_id: int = Path(gt=0)):
    house_changed = False
    for i in range(len(HOUSES)):
        if HOUSES[i].id == house_id:
            HOUSES.pop(i)
            house_changed = True
            break
    if not house_changed:
        raise HTTPException(status_code=404, detail="House not found")
