import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from project.config import settings

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_CONNECTION_STRING)


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/health_check/")
def health_check():
    return "ok"


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        debug=settings.DEBUG,
        port=settings.PORT,
        access_log=settings.ACCESS_LOG,
    )
