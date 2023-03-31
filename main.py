import uvicorn
from fastapi import FastAPI

from app.db.schemas import Base
from app.dependencies import DependencyContainer

from app.api import user

app = FastAPI()

app.include_router(user.router)

if __name__ == "__main__":
    DependencyContainer.initialize_container()
    # Base.metadata.create_all(DependencyContainer.ENGINE)
    uvicorn.run(app, host="0.0.0.0", port=5000)
