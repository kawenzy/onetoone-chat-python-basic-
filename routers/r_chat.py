from fastapi import APIRouter
from fastapi.requests import Request
from schemas import Chat
from controllers import createchat, fchat

chatRoute = APIRouter()

@chatRoute.post("/chat/add/{rid}",tags=["chat"])
async def createdchat(request: Request,chat: Chat, rid: int):
    return await createchat(rid=rid, chat=chat,req=request)

@chatRoute.get("/chat/get/{rid}", tags=["chat"])
async def getchat(request: Request, rid: int):
    return await fchat(req=request, rid=rid)