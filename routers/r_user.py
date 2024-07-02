from fastapi import APIRouter
from fastapi.requests import Request
from controllers import createaccount,logins,logout
from schemas import RUser,LUser

userRoute = APIRouter()

@userRoute.post("/register",tags=["auth"])
async def register(request: Request, user: RUser):
    return await createaccount(req=request, user=user)

@userRoute.post("/login", tags=["auth"])
async def login(request: Request, user: LUser):
    return await logins(req=request,user=user)

@userRoute.post("/logout",tags=["user"])
async def logouts(request: Request):
    return await logout(req=request)