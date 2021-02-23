import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.api.controller import transfer

app = FastAPI(title="Transfer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

api_route = APIRouter()
api_route.include_router(transfer.route, prefix="/transfer", tags=["transfer"])
app.include_router(api_route, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)