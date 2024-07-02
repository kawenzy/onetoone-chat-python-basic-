from fastapi import FastAPI
from utils import prisma
import uvicorn
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from routers import userRoute, chatRoute

description = """
free example one to one chat api. 🚀
---------------------------------------------
##  from kawenzy `https://github.com/kawenzy`
---------------------------------------------
just example api only not advance, this is better for beginner
"""

app = FastAPI(description=description)

origins = [
    "http://127.0.0.1:4000",
]

routes = [userRoute,chatRoute]
for rouute in routes:
    app.include_router(router=rouute, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"hello": "world"}

async def main():
    await prisma.connect()
    config = uvicorn.Config("main:app", port=4000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())