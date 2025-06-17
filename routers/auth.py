from fastapi import APIRouter,Response
from schema.user import SignInRequest,SignUpRequest
from controller.user import signin , signup

app = APIRouter()

@app.post("/signin")
async def signin_route(data : SignInRequest):
    try:
        return await signin(data)
    except Exception as e:
        print(e)
        raise e

@app.post("/signup")
async def signup_route(data : SignUpRequest,response : Response):
    try:
        return await signup(data , response)
    except Exception as e:
        print(e)
        raise e
# @app.get("/signup")
# async def get_all_user():
#     try:
#         return await get_user()
#     except Exception as e:
#         print(e)
#         return {"error" : e}

# @app.get("/signout")
# async def get_all_user():
#     try:
#         return await get_user()
#     except Exception as e:
#         print(e)
#         return {"error" : e}
    