from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

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


# @app.get("/items")
# async def list_items():
#     return {"message": "list items route"}


# @app.get("/items/{item_id}")
# # Specify an expected type of data
# async def get_item(item_id: int):
#     return {"item_id": item_id}


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


# Query parameters section


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Bus"},
]


@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
# required query parameter sample_query_parameter
async def get_item(
    item_id: str, sample_query_param, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "sample_query_param": sample_query_param}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "Lorem ipsum dolor"})
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "Lorem ipsum dolor"})
    return item


# Request body section


class Item(BaseModel):
    name: str
    description: str
    price: float
    # Optional |
    tax: float | None = None


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
