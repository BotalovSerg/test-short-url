import os
import uvicorn
from fastapi import FastAPI

from api import router

app = FastAPI()

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8080))

app.include_router(router=router, prefix="/v1")

if __name__ == "__main__":

    uvicorn.run(app, host=HOST, port=PORT)
