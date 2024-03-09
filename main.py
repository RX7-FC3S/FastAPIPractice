import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_all_tables


from api.item.api import router as item_router


# fastapi 的生命周期函数
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)

# 添加路由
app.include_router(item_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
