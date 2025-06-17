from fastapi import FastAPI,Depends
import uvicorn
from routers.auth import app as auth_router
from routers.user import app as user_router
from middleware.auth import authentication
from contextlib import asynccontextmanager
from client.pg import init_db_pool,close_db_connection
from fastapi.middleware.cors import CORSMiddleware



origins = [
    "http://localhost",
    "http://localhost:4000",
    "https://your-frontend-domain.com",
]

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db_pool()
    print("🚀 DB Pool created")
    yield
    await close_db_connection()
    print("cloing connection")
    

app = FastAPI(lifespan= lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,           
    allow_methods=["*"],              
    allow_headers=["*"],              
)

# app.include_router(user_router , prefix="/user")
@app.get("/health")
async def health_router():
    return {"status" : "ok"}
app.include_router(auth_router , prefix="/auth")
app.include_router(user_router , prefix="/user" , dependencies=[Depends(authentication)])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)