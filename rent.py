from flask import Flask, jsonify, request
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

app = Flask(__name__)


# House model
class House:
    def __init__(self, id, name, owner, description, rating, published_date):
        self.id = id
        self.name = name
        self.owner = owner
        self.description = description
        self.rating = rating
        self.published_date = published_date

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "description": self.description,
            "rating": self.rating,
            "published_date": self.published_date,
        }


# House Request model
class HouseRequest(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(min_length=3)
    owner: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)


# Initial list of houses
HOUSES = [
    House(1, "Sunny Villa", "John Doe", "A beautiful villa with a sunny view.", 5, 2030),
    House(2, "Cozy Apartment", "Jane Smith", "A cozy apartment in the city center.", 4, 2029),
    House(3, "Luxury Penthouse", "Sam Wilson", "A luxurious penthouse with modern amenities.", 5, 2028),
    House(4, "Budget Studio", "Alex Brown", "An affordable studio for rent.", 3, 2027),
    House(5, "Beach House", "Chris Green", "A house near the beach with scenic views.", 4, 2026),
    House(6, "Mountain Retreat", "Taylor White", "A retreat in the mountains.", 2, 2025),
]


# Helper function
def find_house_id(house):
    house.id = 1 if len(HOUSES) == 0 else HOUSES[-1].id + 1
    return house


# Routes

@app.route("/houses", methods=["GET"])
def read_all_houses():
    return jsonify([house.to_dict() for house in HOUSES]), 200


@app.route("/houses/<int:house_id>", methods=["GET"])
def read_house(house_id):
    for house in HOUSES:
        if house.id == house_id:
            return jsonify(house.to_dict()), 200

    return jsonify({"detail": "House not found"}), 404


@app.route("/houses/rating", methods=["GET"])
def read_houses_by_rating():
    house_rating = request.args.get("house_rating", type=int)

    if not house_rating or house_rating < 1 or house_rating > 5:
        return jsonify({"detail": "Rating must be between 1 and 5"}), 400

    houses_to_return = [
        house.to_dict() for house in HOUSES if house.rating == house_rating
    ]

    return jsonify(houses_to_return), 200


@app.route("/houses/publish", methods=["GET"])
def read_houses_by_publish_date():
    published_date = request.args.get("published_date", type=int)

    if not published_date or published_date < 2000 or published_date > 2030:
        return jsonify({"detail": "Published date must be between 2000 and 2030"}), 400

    houses_to_return = [
        house.to_dict()
        for house in HOUSES
        if house.published_date == published_date
    ]

    return jsonify(houses_to_return), 200


@app.route("/create-house", methods=["POST"])
def create_house():
    try:
        house_request = HouseRequest(**request.json)

        new_house = House(
            id=house_request.id,
            name=house_request.name,
            owner=house_request.owner,
            description=house_request.description,
            rating=house_request.rating,
            published_date=house_request.published_date,
        )

        HOUSES.append(find_house_id(new_house))

        return jsonify({"message": "House created successfully"}), 201

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400


@app.route("/houses/update_house", methods=["PUT"])
def update_house():
    try:
        house_data = HouseRequest(**request.json)

        for i in range(len(HOUSES)):
            if HOUSES[i].id == house_data.id:
                HOUSES[i] = House(
                    id=house_data.id,
                    name=house_data.name,
                    owner=house_data.owner,
                    description=house_data.description,
                    rating=house_data.rating,
                    published_date=house_data.published_date,
                )

                return jsonify({"message": "House updated successfully"}), 200

        return jsonify({"detail": "House not found"}), 404

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400


@app.route("/houses/<int:house_id>", methods=["DELETE"])
def delete_house(house_id):
    for i in range(len(HOUSES)):
        if HOUSES[i].id == house_id:
            HOUSES.pop(i)
            return jsonify({"message": "House deleted successfully"}), 200

    return jsonify({"detail": "House not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
