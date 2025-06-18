from schema.user import SignInRequest,SignUpRequest,updateUserRequest
from fastapi import HTTPException, status, Response,Request
from accessor.auth import get_user_from_email,add_user,update_user_from_id
from utils.index import hash_password,verify_password , generate_token
async def  signin(data : SignInRequest,response : Response):
    password = data.password
    email = data.email
    if not password or not email:
        print("missing")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )
    
    user = await get_user_from_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is not registered"
        )
    verified_user = verify_password(password , user["password"])
    print(verified_user , " verified user")
    if not verified_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Password"
        )
    
    del user["password"]
    token = generate_token(user)
    response.set_cookie(
        key="token",
        value=token, 
        httponly=True,
        max_age=3600,
        secure=False,       
        samesite="None" 
    )
    return {"token" : token , "user" : user}
    
    
async def  signup(data : SignUpRequest,response : Response):
    password = data.password
    email = data.email
    name = data.name
    if not password or not email or not name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Data"
        )
    
    existing_user = await get_user_from_email(email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    hashed_password = hash_password(password)
    token = generate_token({"email" : email , "name" : name})
    
    user = await add_user({"email" : email , "name" : name , "password" : hashed_password})
    del user["password"]
    response.set_cookie(
        key="token",
        value=token, 
        httponly=True,
        max_age=3600,
        secure=True,       
        samesite="None" 
    )
    return {"user": user}

async def update_user(data: updateUserRequest,request :Request):
    user = request.state.user
    user_data_to_update = {}
    fields = ["name" , "password"]
    print(data , " data")
    for key in fields:
        value = getattr(data, key, None)
        if value:
            user_data_to_update[key] = value
    if "password" in user_data_to_update:
        user_data_to_update["password"] = hash_password(user_data_to_update["password"])
    # print(user_data_to_update , " data to modify")
    updated_user = await update_user_from_id(user["id"],user_data_to_update)
    return updated_user