# import fastapi
from fastapi import FastAPI
from enum import Enum

# create a FastAPI instance
app = FastAPI()

# define a path operation decorator
#  the @app.get() tells fastapi that the function below is in charge of handling a get requests that go to the path "/" using a get operation
@app.get("/")
# define the function that will handle the request
def read_root():
    return {"message" : "Hello world!"}

# path parameters or variables with type hints
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item id": item_id}

# Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:
@app.get("/users/me")
def read_current_user():
    return {"current user": "me"}

# path parameters or variables without type hints
@app.get("/users/{user}")
def read_user(user):
    return {"user": user}

# if below code is uncommented, then the path operation for /users/me will be evaluated before the one for /users/{user_id} so make sure that the path for /users/me is declared before the one for /users/{user_id} cuz the order matters
# Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me".

# @app.get("/users/me")
# def read_current_user():
#     return {"current user": "me"}

# Similarly, you cannot redefine a path operation:
# The first one will always be used since the path matches first.
@app.get("/users")
def get_allUsers():
    return {"all users": "users"}

@app.get("/users")
def get_users():
    return {"all users 2": "users"}

# Predefined values - If you have a path operation that receives a path parameter, but you want the possible valid path parameter values to be predefined, you can use a standard Python Enum.

class ModelName(str, Enum):
    alfa = "Alfa"
    beta = "Beta"
    gamma = "Gamma"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName): #Declare a path parameter Then create a path parameter with a type annotation using the enum class you created (ModelName):
    if model_name is ModelName.alfa:
        return {"model_name" : model_name, "message" : "Alfa model"}
    
    if model_name.value == "beta":
        return {"model_name" : model_name, "message" : "Beta model"}
    
    return {"model_name" : model_name, "message" : "Gamma model"}

# file path
@app.get("file/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path" : file_path}

# query parameters
# The query parameter is the value that comes after the ? in the URL.
# When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.
# http://127.0.0.1:8000/items/?skip=0&limit=10
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# the query parameters are: skip: with a value of 0 and limit: with a value of 10
# As they are part of the URL, they are "naturally" strings.
# But when you declare them with Python types (in the example above, as int), they are converted to that type and validated against it.
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

# DEFAULT VALUES
# As query parameters are not a fixed part of a path, they can be optional and can have default values.
# If you don't pass a query parameter, the default value will be used. so if you pass http://127.0.0.1:8000/items then the default values will be used which is http://127.0.0.1:8000/items/?skip=0&limit=10 
# but if you pass ?skip=20 then http://127.0.0.1:8000/items/?skip=20&limit=10 will be used cuz the default value of limit is 10 and skip is 20 as you passed.

# OPTIONAL VALUES
# the same way you can declare optional qyery parameters, by setting there default to None.
# in this case, if you don't pass ?skip=20 then http://127.0.0.1:8000/items/?limit=10 will be used
@app.get("/items/optional/")
async def read_optional_items(skip: int = None, limit: int = 10):
    if skip is not None:
        return fake_items_db[skip: skip + limit]
    return fake_items_db

# Also notice that FastAPI is smart enough to notice that the path parameter item_id is a path parameter and q is not, so, it's a query parameter.
@app.get("/items/optional/{item_id}")
def read_item(item_id: str, q: str | None = None):
    if(q):
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# QUERY PARAMETES TYPE CONVERSION
# you can also create bool types, they will be converted to True or False
@app.get("/items/bool/{item_id}")
def read_bool_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if short:
        item.update({"desciption": "The description of the item is short"})
    if not short:
        item.update({"desciption": "The description of the item is long"})
    return item
# in this case, if you go to http://127.0.0.1:8000/items/bool/1?short=True or http://127.0.0.1:8000/items/bool/1?short=true or http://127.0.0.1:8000/items/bool/1?short=1 or http://127.0.0.1:8000/items/bool/?short=yes or http://127.0.0.1:8000/items/bool/?short=on or any other case variation (uppercase, first letter in uppercase, etc), your function will see the parameter short with a bool value of True. Otherwise as False.   

# MULTIPLE PATH AND QUERY PARAMETERS
# you can have multiple path and query parameters in a single function
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str|None = None, short:bool=False):
    user = {"user_id": user_id, "item_id": item_id}
    if q:
        user.update({"q": q})
    if short:
        user.update({"desciption": "The description of the item is short"})
    if not short:
        user.update({"desciption": "The description of the item is long"})
    return user

# REQUIRED QUERY PARAMETERS
# you can also declare required query parameters
# if you don't pass a required query parameter, you will get an error
# the error message will be: "Path parameter 'q' is required"
# When you declare a default value for non-path parameters (for now, we have only seen query parameters), then it is not required.
# If you don't want to add a specific value but just make it optional, set the default as None.
# But when you want to make a query parameter required, you can just not declare any default value
# here needy is a required query parameter
@app.get("/item/required/{item_id}/")
async def read_required_item(item_id: int, needy: str):
    return {"item": item_id, "needy": needy}
# if you do not pass needy, you will get an error {"detail":[{"type":"missing","loc":["query","item"],"msg":"Field required","input":null},{"type":"missing","loc":["query","needy"],"msg":"Field required","input":null}]}

# REQUEST BODY
# when you need to send data from client to your API/server, you send it as request body
# a request body is data sent by the client to your API.
# a response body is data your API sends to the client