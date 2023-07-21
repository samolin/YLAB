from fastapi import FastAPI

from app.db.base import Base
from app.db.database import engine
from app.core.config import settings

app = FastAPI()


@app.get("/")
async def test():
    return {"message": "hello world"}


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_VERSION,
    )
    create_tables()
    return app


app = start_application()



