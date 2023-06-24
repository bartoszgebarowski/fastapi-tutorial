from fastapi import FastAPI

app = FastAPI()


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
