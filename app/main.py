import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import configure_mappers
from dotenv import load_dotenv

from app.api.v1 import organization_route, auth_route, contact_route
from app.logging_conf import setup_logging
from app.middleware import CorrelationIdASGIMiddleware

setup_logging()




def create_app() -> FastAPI:
    app = FastAPI(title="FitnessApp API", version="0.1.0")
    app.add_middleware(
        CorrelationIdASGIMiddleware,
        request_body_limit=8 * 1024,
        response_body_limit=8 * 1024,
        log_headers=False,
    )
    app.include_router(auth_route.router, prefix="/api")
    app.include_router(organization_route.router, prefix="/api")
    app.include_router(contact_route.router, prefix="/api")
    # app.include_router(workout.router, prefix="/api/v1/workouts", tags=["workouts"])
    # app.include_router(group.router, prefix="/api/v1/groups", tags=["groups"])

    return app


app = create_app()

if __name__ == "__main__":
    configure_mappers()

    load_dotenv()
    uvicorn.run("main:app", host="0.0.0.0", port=5050, reload=True)
