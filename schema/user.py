from pydantic import BaseModel
from typing import Optional

class SignInRequest(BaseModel):
    email: str
    password: str

class SignUpRequest(BaseModel):
    email: str
    password: str
    name : str

class updateUserRequest(BaseModel):
    password: Optional[str] = None
    name :  Optional[str] = None