from fastapi import APIRouter,Request
from schema.user import updateUserRequest
from controller.user import update_user

app = APIRouter()

@app.get("/")
async def get_user_route(request:Request):
    print(request.state)
    return {"user" : request.state.user}


@app.put("/update")
async def update_user_route(data : updateUserRequest, request:Request):
    try:
        return await update_user(data,request)
    except Exception as e:
        raise e



