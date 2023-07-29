from fastapi import FastAPI

from app.db.base import Base
from app.db.database import engine
from app.core.config import settings
from app.routers.base import api_router

app = FastAPI()


def include_routers(app):
    app.include_router(api_router)

def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_VERSION,
    )
    create_tables() 
    include_routers(app)
    return app


app = start_application()
