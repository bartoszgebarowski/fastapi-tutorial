from enum import Enum

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field

app = FastAPI()


# Part 1 -> Initial Setup

# @app.get("/")
# async def root():
#     return {"message": "hello world"}

# @app.get("/base", description="This is my first route", deprecated=True)
# async def base_get_route():
#     return {
#         "message": "base route with description and deprecated set to True"
#     }

# @app.post("/")
# async def post():
#     return {"message": "hello from the post route"}


# @app.put("/")
# async def put():
#     return {"message": "hello from the put route"}


# @app.get("/items")
# async def list_items():
#     return {"message": "list items route"}


# @app.get("/items/{item_id}")
# # Specify an expected type of data
# async def get_item(item_id: int):
#     return {"item_id": item_id}

# Part 2 -> Path parameters section

# @app.get("/users")
# async def get_users():
#     return {"message": "list items route"}


# Allow specific endpoint before dynamic endpoint
# @app.get("/users/me")
# async def get_current_user():
#     return {"Message": "This is the current user"}


# @app.get("/users/{user_id}")
# async def get_user(user_id: int):
#     return {"user_id": user_id}

# class FoodEnum(str, Enum):
#     fruits = "fruits"
#     vegetables = "vegetables"
#     dairy = "dairy"

# @app.get("/foods/{food_name}")
# async def get_food(food_name: FoodEnum):
# by class type
# if food_name == FoodEnum.vegetables:
#     return {"food_name": food_name, "message": "you are healthy"}
# by value passed
# if food_name.value == "fruits":
#     return {
#         "food_name": food_name,
#         "message": "you are still healthy, but like other things",
#     }
# return {"food_name": food_name, "message": "i like gouda"}

# Part 3 -> Query parameters section

# fake_items_db = [
#     {"item_name": "Foo"},
#     {"item_name": "Bar"},
#     {"item_name": "Bus"},
# ]

# @app.get("/items")
# async def list_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]


# @app.get("/items/{item_id}")
# required query parameter sample_query_parameter
# async def get_item(
#     item_id: str, sample_query_param, q: str | None = None, short: bool = False
# ):
#     item = {"item_id": item_id, "sample_query_param": sample_query_param}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update({"description": "Lorem ipsum dolor"})
#     return item

# @app.get("/users/{user_id}/items/{item_id}")
# async def get_user_item(
#     user_id: int, item_id: str, q: str | None = None, short: bool = False
# ):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update({"description": "Lorem ipsum dolor"})
#     return item

# Part 4 -> Request body section

# class Item(BaseModel):
#     name: str
#     description: str
#     price: float
#     # Optional |
#     tax: float | None = None

# @app.post("/items")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# @app.put("/items/{item_id}")
# async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result

# Part 5 -> Query params and string validation

# @app.get("/itemsquery/")
# required with validation  ...
# async def read_items(
#     q: list[str] | None = Query(..., min_length=3, max_length=10)
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/itemsquerymeta/")
# async def read_items_meta_data(
#     q: str
#     | None = Query(
#         None,
#         min_length=3,
#         max_length=10,
#         title="Sample",
#         description="This is sample query string",
#         alias="item-query",
#     )
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# @app.get("/items_hidden")
# async def hidden_query_route(
#     hidden_query: str | None = Query(None, include_in_schema=False)
# ):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     return {"hidden_query": "Not found"}

# Part 6 -> Path params and numeric validation section

# @app.get("/items_validation/{item_id}")
# * as first argument, the rest is kwargs
# Swagger bug - will not display conditions all conditions
# async def read_items_validation(
#     *,
#     item_id: int = Path(..., title="The ID of the item to get", gt=10, le=100),
#     q: str = "hello",
#     size: float = Query(..., gt=0, lt=7.75)
# ):
#     results = {"item_id": item_id, "size": size}
#     if q:
#         results.update({"q": q})
#     return results


# Part 7 -> Body - Multiple Parameters
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# class User(BaseModel):
#     username: str
#     full_name: str | None = None


# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int = Path(..., title="The id of the item to get", ge=0, le=150),
#     q: str | None = None,
#     item: Item = Body(..., embed=True),
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     return results

# Part 8 -> Body Field


class Item(BaseModel):
    name: str
    description: str | None = Field(
        None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="Must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results
