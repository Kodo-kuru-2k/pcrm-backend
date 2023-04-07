import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.dependencies import DependencyContainer

from app.api import user, common, power_user, admin_user

app = FastAPI()

app.include_router(common.router)
app.include_router(user.router)
app.include_router(power_user.router)
app.include_router(admin_user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    DependencyContainer.initialize_container()
    uvicorn.run(app, host="localhost", port=5000)
