import uvicorn
from fastapi import FastAPI

from project.config import settings
from project.api.routes import partner_routes

app = FastAPI()


@app.get("/health_check/")
def health_check() -> str:
    return "ok"


app.include_router(partner_routes.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        debug=settings.DEBUG,
        port=settings.PORT,
        access_log=settings.ACCESS_LOG,
    )
