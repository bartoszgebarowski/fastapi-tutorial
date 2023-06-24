from enum import Enum

from fastapi import FastAPI

app = FastAPI()

# Initial setup


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/base", description="This is my first route", deprecated=True)
async def base_get_route():
    return {
        "message": "base route with description and deprecated set to True"
    }


@app.post("/")
async def post():
    return {"message": "hello from the post route"}


@app.put("/")
async def put():
    return {"message": "hello from the put route"}


@app.get("/items")
async def list_items():
    return {"message": "list items route"}


@app.get("/items/{item_id}")
# Specify an expected type of data
async def get_item(item_id: int):
    return {"item_id": item_id}


# Path parameters section


@app.get("/users")
async def get_users():
    return {"message": "list items route"}


# Allow specific endpoint before dynamic endpoint
@app.get("/users/me")
async def get_current_user():
    return {"Message": "This is the current user"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}


class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"


@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    # by class type
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message": "you are healthy"}
    # by value passed
    if food_name.value == "fruits":
        return {
            "food_name": food_name,
            "message": "you are still healthy, but like other things",
        }
    return {"food_name": food_name, "message": "i like gouda"}
