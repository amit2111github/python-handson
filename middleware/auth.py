from fastapi import Request, HTTPException, status
from utils.index import verify_jwt
from accessor.auth import get_user_from_email

async def authentication(request: Request):
    token = request.cookies.get("token") 
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    payload = verify_jwt(token)

    if "error" in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=payload["error"])
    print(payload)
    user = await get_user_from_email(payload["email"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    del user["password"]
    request.state.user = user 
