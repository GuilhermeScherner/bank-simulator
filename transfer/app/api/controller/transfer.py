from fastapi import APIRouter
from starlette.middleware.cors import CORSMiddleware


route = APIRouter()


@route.get("")
def get_transfer():
    return