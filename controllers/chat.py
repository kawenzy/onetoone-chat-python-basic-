from utils import curruser, prisma
from schemas import Chat
from fastapi.responses import JSONResponse
from fastapi import Body, status
from fastapi.requests import Request
from typing import Annotated

async def createchat(chat: Annotated[Chat, Body(embed=True)],req: Request, rid: int):
    cook = req.cookies.get("token")
    if not cook:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "login is required"})
    chekctook = await prisma.user.find_many(where={"token": cook})
    if not chekctook:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "login is required"})
    user = curruser(req=req)
    uuid = user["id"]
    data = {
        "sendID": uuid,
        "msg": chat.msg,
        "receiverId": rid
    }
    await prisma.chats.create(data=data)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "send chat is succsfully"})

async def fchat(req: Request, rid: int):
    cook = req.cookies.get("token")
    if not cook:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "login is required"})
    chekctook = await prisma.user.find_many(where={"token": cook})
    if not chekctook:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "login is required"})
    user = curruser(req=req)
    uuid = user["id"]
    mchat = await prisma.chats.find_many(where={"receiverId": uuid})
    ychat = await prisma.chats.find_many(where={"receiverId": rid})
    ckchat = list(filter((lambda u: rid == u.sendID), mchat))
    ykchat = list(filter((lambda u: uuid == u.sendID), ychat))
    # ini semua yang dibawah salah, yang saya jadikn comment
    # receiver = await prisma.chats.find_many()
    # if not ckchat:
    #     return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content={"message": "haven't sent a message yet"})
    # if not ykchat:
    #     return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content={"message": "haven't sent a message yet"})
    # rchat = list(filter((lambda u: rid == u.receiverId), receiver))
    # schat = list(filter((lambda u: uuid == u.receiverId), receiver))
    sc = ckchat + ykchat 
    sortchat = sorted(sc, key=lambda x: x.createdAt)
    if not sc:
        return JSONResponse(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, content={"message": "haven't sent a message yet"})
    data = [{
        "id": d.id,
        "sendID": d.sendID,
        "msg": d.msg,
        "receiverId": d.receiverId,
        "createdAt": d.createdAt.isoformat(),
        "updatedAt": d.updatedAt.isoformat()
    }for d in sortchat]
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)