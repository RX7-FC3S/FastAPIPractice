import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_all_tables


# fastapi 的生命周期函数
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)

# 添加路由
from services.basic_data.item.item_info.api import router as router_item_info
from services.basic_data.layout.bin_spec.api import router as router_bin_spec
from services.basic_data.layout.bin_info.api import router as router_bin_info

app.include_router(router_item_info)
app.include_router(router_bin_spec)
app.include_router(router_bin_info)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
