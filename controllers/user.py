from fastapi.responses import JSONResponse
from fastapi import Body, status
from passlib.context import CryptContext
from fastapi.requests import Request
from schemas import RUser, LUser
from typing import Annotated
from utils import prisma, curruser
import jwt



async def createaccount(user: Annotated[RUser, Body(embed=True)], req: Request):
    if len(str(user.password)) < 6 :
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "password is required 6 lenght minimals"})
    checkemail = await prisma.user.find_unique(where={"email": user.email})
    if checkemail:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "already email"})
    took = req.cookies.get("token")
    if took:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "Can't create an account because you're logged in"})
    pw = CryptContext(schemes=["sha256_crypt"])
    pw.default_scheme()
    data = {
        "name": user.name,
        "email": user.email,
        "password": pw.hash(user.password),
    }
    await prisma.user.create(data=data)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "create account succesfully"})

def tokens(payload: dict, secret: str, algo: str):
    return jwt.encode(payload=payload,key=secret,algorithm=algo)

async def logins(req: Request, user: Annotated[LUser, Body(embed=True)]):
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    checktoken = await prisma.user.find_unique(where={"email": user.email})
    if checktoken.token:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "already login"})
    chekcookies = req.cookies.get("token")
    if chekcookies:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "already login"})
    pw = CryptContext(schemes=["sha256_crypt"])
    pw.default_scheme()
    users = await prisma.user.find_unique(where={"email": user.email})
    if not users:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"msg": "user not found"})
    passw = pw.verify(user.password, users.password)
    if not passw:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "password is wrong"})
    payload = {
        "id": users.id,
        "name": users.name,
        "email": users.email
    }
    token = tokens(payload=payload,secret=SECRET_KEY,algo=ALGORITHM)
    await prisma.user.update(where={"email": user.email},data={"token":token})
    resp = JSONResponse(status_code=status.HTTP_200_OK,content={"msg": "login succes"})
    resp.set_cookie("token",value=token)
    return resp


async def logout(req: Request):
    checktoken = req.cookies.get("token")
    if not checktoken:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"msg": "login is required"})
    find = await prisma.user.find_many(where={"token": checktoken})
    if not find:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"msg": "login is required"})
    curr = curruser(req=req)
    uuid = curr["id"]
    await prisma.user.update(where={"id": uuid},data={"token": None})
    respon = JSONResponse(status_code=status.HTTP_200_OK,content={"msg": "logout succes"})
    respon.delete_cookie("token")
    return respon