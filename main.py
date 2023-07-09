from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID
import time
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
    Depends,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from passlib.context import CryptContext
from jose import jwt, JWTError

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


# class Item(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     price: float | None = None
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


# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items.get(item_id)


# @app.put("/items/{item_id}", response_model=Item)
# def update_item(item_id: str, item: Item):
#     update_item_encoded = jsonable_encoder(item)
#     items[item_id] = update_item_encoded
#     return update_item_encoded


# @app.patch("/items/{item_id}", response_model=Item)
# def patch_item(item_id: str, item: Item):
#     stored_item_data = items.get(item_id)
#     if stored_item_data is not None:
#         stored_item_model = Item(**stored_item_data)
#     else:
#         stored_item_model = Item()
# IMPORTANT !!! EXCLUDE
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     return updated_item


# PART 22 -> Dependencies intro
# async def common_parameters(
#     q: str | None = None, skip: int = 0, limit: int = 100
# ):
#     return {"q": q, "skip": skip, "limit": limit}


# @app.get("/items/")
# # common params returns dict
# async def read_items(commons: dict = Depends(common_parameters)):
#     return commons


# @app.get("/users/")
# async def read_users(commons: dict = Depends(common_parameters)):
#     return commons

# Part 23 -> Classes as dependencies

# fake_items_db = [
#     {"item_name": "Foo"},
#     {"item_name": "Bar"},
#     {"item_name": "Baz"},
# ]


# class CommonQueryParams:
#     def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
#         self.q = q
#         self.skip = skip
#         self.limit = limit


# @app.get("/items/")
# async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
#     response = {}
#     if commons.q:
#         response.update({"q": commons.q})
#     items = fake_items_db[commons.skip : commons.skip + commons.limit]
#     response.update({"items": items})
#     return response


# Part 24 -> Classes as dependencies
# def query_extractor(q: str | None = None):
#     return q


# def query_or_body_extractor(
#     q: str = Depends(query_extractor), last_query: str | None = Body(None)
# ):
#     if not q:
#         return last_query
#     else:
#         return q


# @app.post("item")
# async def try_query(query_or_body: str = Depends(query_or_body_extractor)):
#     return {"q_or_body": query_or_body}

# Part 25 -> Dependencies in path operation decorators, global dependencies
# async def verify_token(x_token: str = Header(...)):
#     if x_token != "fake-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")


# async def verify_key(x_key: str = Header(...)):
#     if x_key != "fake-key":
#         raise HTTPException(status_code=400, detail="X-Key Header invalid")
#     return x_key


# # Global dependencies
# app = FastAPI(dependencies=[Depends(verify_key), Depends(verify_token)])

# # if you want use key in a function don't put it into a decorator
# @app.get("/items/")
# async def read_items():
#     return [{"item": "Foo"}, {"item": "bar"}]


# @app.get("/users/")
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]

## Part 26 - Security, First Steps
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# fake_users_db = {
#     "johndoe": dict(
#         username="johndoe",
#         full_name="John Doe",
#         email="johndoe@example.com",
#         hashed_password="fakehashedsecret",
#         disabled=False,
#     ),
#     "alice": dict(
#         username="alice",
#         full_name="Alice Wonderson",
#         email="alice@example.com",
#         hashed_password="fakehashedsecret2",
#         disabled=True,
#     ),
# }


# def fake_hash_password(password: str):
#     return f"fakehashed{password}"


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def fake_decode_token(token):
#     return get_user(fake_users_db, token)


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


# async def get_current_active_user(
#     current_user: User = Depends(get_current_user),
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(
#             status_code=400, detail="Incorrect username or password"
#         )
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(
#             status_code=400, detail="Incorrect username or password"
#         )

#     return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/users/me")
# async def get_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

# Part 27 -> Security with JWT

## Part 27 - Security, OAuth2 Bearer and JWT
# SECRET_KEY = "thequickbrownfoxjumpedoverthelazydog"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$tJD64mRe0bd/UNdAANZtvuOnWDKScbVtXA9lB6X7arZxJQbAyMbd2",
#         "disabled": False,
#     }
# }


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: str | None = None


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not User:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(
#     current_user: User = Depends(get_current_user),
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive User")
#     return current_user


# @app.post("/token", response_model=Token)
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
# ):
#     user = authenticate_user(
#         fake_users_db, form_data.username, form_data.password
#     )
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/me", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/users/me/items")
# async def read_own_items(
#     current_user: User = Depends(get_current_active_user),
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]

# Part 28 -> Middleware and CORS


class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


origins = ["http://localhost:8000", "http://localhost:3000"]
app.add_middleware(MyMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=origins)


@app.get("/smth")
async def smth():
    return {"hello": "world"}
