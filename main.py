from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID

from fastapi import (
    Body,
    Cookie,
    FastAPI,
    File,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from starlette.exceptions import HTTPException as StarletteHTTPException

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


# class Item(BaseModel):
#     name: str
#     description: str | None = Field(
#         None, title="The description of the item", max_length=300
#     )
#     price: float = Field(..., gt=0, description="Must be greater than zero")
#     tax: float | None = None


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(..., embed=True)):
#     results = {"item_id": item_id, "item": item}
#     return results


## Part 9 -> Nested models
# class Image(BaseModel):
#     # Pydantic httpurl validation
#     url: HttpUrl
#     name: str


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: list[str] = []
#     image: list[Image] | None = None


# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     items: list[Item]


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results


# @app.post("/offers")
# async def create_offer(offer: Offer = Body(..., embed=True)):
#     return offer


# @app.post("/images/multiple")
# async def create_multiple_images(images: list[Image] = Body(..., embed=True)):
#     return images


# @app.post("/anotherone")
# async def create_example(example: dict[int, float]):
#     return example

# Part 10 -> Declare request example data

# class Item(BaseModel):
#     name: str = Field(..., example='Foo')
#     description: str | None = Field(None, example="Item desc")
#     price: float = Field(..., example=16.25)
#     tax: float | None = Field(None, example=1.67)

# class Config:
#     schema_extra = {
#         "example": {
#             "name": "Foo",
#             "description": "Item description",
#             "price": 12.25,
#             "tax": 1.67
#         }
#     }


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Item = Body(
#         ...,
#         examples={
#             "normal": {
#                 "summary": "A normal example",
#                 "description": "A __normal__ item works _correctly_",
#                 "value": {
#                     "name": "Foo",
#                     "description": "Normal desc item",
#                     "price": 16.25,
#                     "tax": 1.67,
#                 },
#             },
#             "converted": {
#                 "summary": "An example with converted data",
#                 "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
#                 "value": {"name": "Bar", "price": "16.25"},
#             },
#             "invalid": {
#                 "summary": "Invalid data is rejected with an error",
#                 "description": "Example desc",
#                 "value": {"name": "JJ", "price": "sixteen point two five"},
#             },
#         },
#     ),
# ):
#     results = {"item_id": item_id, "item": item}
#     return results

# Part 11 -> Extra Data types


# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_date: datetime | None = Body(None),
#     end_date: datetime | None = Body(None),
#     repeat_at: time | None = Body(None),
#     process_after: timedelta | None = Body(None),
# ):
#     start_process = start_date + process_after
#     duration = end_date - start_process
#     return {
#         "item_id": item_id,
#         "start_date": start_date,
#         "end_date": end_date,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "start_process": start_process,
#         "duration": duration,
#     }

# Part 12 -> Cookie and Header parameters section


# @app.get("/items")
# async def read_items(
#     cookie_id: str | None = Cookie(None),
#     accept_encoding: str | None = Header(None),
#     seo_ch_ua: str | None = Header(None),
#     user_agent: str | None = Header(None),
#     x_token: list[str] | None = Header(None),
# ):
#     return {
#         "cookie_id": cookie_id,
#         "Accept-Encoding": accept_encoding,
#         "sec-ch-ua": seo_ch_ua,
#         "User_Agent": user_agent,
#         "X-Token values": x_token,
#     }


# Part 13 -> Response model
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5
#     tags: list[str] = []


# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {
#         "name": "Bar",
#         "description": "The bartenders",
#         "price": 62,
#         "tax": 20.2,
#     },
#     "baz": {
#         "name": "Baz",
#         "description": None,
#         "price": 50.2,
#         "tax": 10.5,
#         "tags": [],
#     },
# }


# @app.get(
#     "/items/{item_id}", response_model=Item, response_model_exclude_unset=True
# )
# async def read_item(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]


# @app.post("/items", response_model=Item)
# async def create_item(item: Item):
#     return item


# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# class UserIn(BaseModel):
#     password: str


# class UserOut(UserBase):
#     pass


# @app.post("/user", response_model=UserOut)
# async def create_user(user: UserIn):
#     return user


# @app.get(
#     "/items/{item_id}/name}",
#     response_model=Item,
#     response_model_include={"name", "description"},
# )
# async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]


# @app.get(
#     "items/{item_id}/public",
#     response_model=Item,
#     response_model_exclude={"tax"},
# )
# async def read_items_public_data(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]


# Part 14 -> Extra Models
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# class UserIn(UserBase):
#     password: str


# class UserOut(UserBase):
#     pass


# class UserInDB(UserBase):
#     hashed_password: str


# def fake_password_hasher(raw_password: str):
#     return f"supersecret{raw_password}"


# def fake_save_user(user_in: UserIn):
#     # double star - similar to spread operator in JS
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
#     print("userin.dict", user_in.dict())
#     print("User 'saved'")
#     return user_in_db


# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved


# class BaseItem(BaseModel):
#     description: str
#     type: str


# class CarItem(BaseItem):
#     type = "car"


# class PlaneItem(BaseItem):
#     type = "plane"
#     size: int


# items = {
#     "item1": {"description": "some desc", "type": "car"},
#     "item2": {"description": "desc 2", "type": "plane", "size": 5},
# }


# @app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
# async def read_item(item_id: Literal["item1", "item2"]):
#     return items[item_id]


# class ListItem(BaseModel):
#     name: str
#     description: str


# list_items = [
#     {"name": "Foo", "description": "123"},
#     {"name": "Bar", "description": "456"},
# ]


# @app.get("/list_items/", response_model=list[ListItem])
# async def read_items():
#     return items


# @app.get("/arbitrary", response_model=dict[str, float])
# async def get_arbitrary():
#     return {"foo": 1, "bar": "2"}

# Part 15 -> Response status codes


# @app.post("/items/", status_code=status.HTTP_201_CREATED)
# async def create_item(name: str):
#     return {"name": name}


# @app.delete("/items/{pk}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_item(pk: str):
#     print("pk", pk)
#     # No item in a response
#     return pk


# @app.get("/items1/", status_code=status.HTTP_302_FOUND)
# async def read_items_redirect():
#     # No item in a response


# Part 16 -> Form Fields
# class User(BaseModel):
#     username: str
#     password: str


# @app.post("/login")
# async def login(username: str = Form(...), password: str = Form(...)):
#     print("pass", password)
#     return {"username": username}


# @app.post("/login-json")
# async def login_json(username: str = Body(...), password: str = Body(...)):
#     print("password", password)
#     return username

# Part 17 - Request files


# @app.post("/files")
# async def create_files(
#     files: list[bytes] | None = File(None, description="A file read as bytes")
# ):
#     return {"file_sizes": [len(file) for file in files]}


# @app.post("/uploadfile")
# async def create_upload_file(
#     files: list[UploadFile] = File(
#         ..., description="A file read as uploadfile"
#     )
# ):
#     return {"filename": [file.filename for file in files]}


# @app.get("/")
# async def main():
#     content = """
#     <html>
#         <body>
#             Hello world !
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=content)

# Part 18 Request Forms and Files


# @app.post("/files/")
# async def create_file(
#     file: bytes = File(...),
#     fileb: UploadFile = File(...),
#     token: str = Form(...),
# ):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }

# Part 19 - Handling Errors

# items = {"foo": "bar"}


# @app.get("items/{items_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(
#             status_code=404,
#             detail="Item not found",
#             headers={"X-Error": "My error"},
#         )
#     return {"item": items[item_id]}


# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name


# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code=418, content={"message": f"{exc.name} did something ..."}
#     )


# @app.get("/unicorns/{name}")
# async def read_unicorns(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# @app.get("/validation_items/{item_id}")
# async def read_validation_items(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3")
#     return  {"item_id": item_id}


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(
#     request: Request, exc: RequestValidationError
# ):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
#     )

# class Item(BaseModel):
#     title: str
#     size: int

# @app.post("/items/")
# async def create_item(item: Item):
#     return item


# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f"OMG ! An HTTP error! : {repr(exc)}")
#     return await http_exception_handler(request, exc)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     print(f"OMG ! The client sent invalid data: {exc}")
#     return await request_validation_exception_handler(request, exc)


# @app.get("/new_items/{item_id}")
# async def read_new_items(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope, I dont like 3")
#     return {"item_id": item_id}

# Part 20 -> Operation Configuration


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()


# class Tags(Enum):
#     items = "items"
#     users = "users"


# @app.post(
#     "/items/",
#     response_model=Item,
#     status_code=status.HTTP_201_CREATED,
#     summary="Create an Item",
# description="Create an item with all the information: name; description; price; tax and a set of unique tags",
# response_description="The created item"
# )
# # async def create_item(item: Item):
#     """
#     Create an item with all information:
#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if item doesn't have a tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
# #     return item


# @app.get("/items/", tags=[Tags.items])
# async def read_items():
#     return [{"name": "Foo", "price": 42}]


# @app.get("/users", tags=[Tags.users])
# async def read_users():
#     return [{"username": "Foobaruser"}]


# @app.get("/elements/", tags=[Tags.items], deprecated=True)
# async def read_elements():
#     return [{"item_id": "Foo elements"}]

# Part 21 -> JSON Compatible encoder and Body updates


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {
        "name": "Bar",
        "description": "The bartenders",
        "price": 62,
        "tax": 20.2,
    },
    "baz": {
        "name": "Baz",
        "description": None,
        "price": 50.2,
        "tax": 10.5,
        "tags": [],
    },
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items.get(item_id)


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


@app.patch("/items/{item_id}", response_model=Item)
def patch_item(item_id: str, item: Item):
    stored_item_data = items.get(item_id)
    if stored_item_data is not None:
        stored_item_model = Item(**stored_item_data)
    else:
        stored_item_model = Item()
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
