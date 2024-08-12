import uvicorn
from fastapi import FastAPI
from backend.core.config import settings


from backend.apis.base import api_router


def include_router(app: FastAPI) -> None:
    """ Includes all routes in app

    Args:
        app (FastAPI): FastAPI object
    """    
    app.include_router(router=api_router)

def start_application() -> FastAPI:
    """Starts FastAPI application using title and version settings

    Returns:
        FastAPI: app object
    """    
    app = FastAPI(title = settings.PROJECT_TITLE, version = settings.PROJECT_VERSION)
    include_router(app=app)
    return app


app: FastAPI = start_application()

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=False)