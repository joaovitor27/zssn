from ninja import NinjaAPI

from survivors.api import router as survivors_router

api = NinjaAPI()

api.add_router("", survivors_router, tags=["Survivors"])
