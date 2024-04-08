from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Аутентификация"])


@router.post()
async def register():
    pass


async def login():
    pass
