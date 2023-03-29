import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import scoped_session
from starlette.requests import Request
from starlette.responses import Response

from core.config import app_config
from core.database.core import SessionLocal, Base, engine
from core.auth import models

app = FastAPI()

Base.metadata.create_all(engine)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Create a new database session for each request, and commit the changes at the end of the request.
    """
    response = Response("Internal server error", status_code=500)
    try:
        session = scoped_session(SessionLocal)
        request.state.db = session()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


if __name__ == "__main__":
    uvicorn.run(app_config.FASTAPI_APP,
                host=app_config.HOST_URL,
                port=app_config.HOST_PORT,
                log_level=app_config.FASTAPI_LOG_LEVEL,
                reload=app_config.FASTAPI_APP_RELOAD)
