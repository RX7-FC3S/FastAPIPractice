from fastapi_pagination.utils import disable_installed_extensions_check
from contextlib import asynccontextmanager
from database import create_all_tables
from fastapi import FastAPI
import uvicorn


# fastapi 的生命周期函数
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)

# 添加路由
# - 基础数据
# -- 业务信息
from services.basic_data.business.order_type.api import router as router_order_type
from services.basic_data.business.stakeholder.api import router as router_stakeholder

app.include_router(router_order_type)
app.include_router(router_stakeholder)

# -- 仓库布局
from services.basic_data.layout.warehouse_area.api import router as router_warehouse_area
from services.basic_data.layout.bin_spec.api import router as router_bin_spec
from services.basic_data.layout.bin_info.api import router as router_bin_info

app.include_router(router_warehouse_area)
app.include_router(router_bin_spec)
app.include_router(router_bin_info)


# -- 物料信息
from services.basic_data.item.item_info.api import router as router_item_info

app.include_router(router_item_info)

# -- 物料单位
from services.basic_data.item.item_unit.api import router as router_item_unit

app.include_router(router_item_unit)

# - 入库管理
# -- 入库订单
# --- 入库订单头
from services.inbound.receiving_list.receiving_list_header.api import router as router_receiving_list_header

app.include_router(router_receiving_list_header)

# --- 入库订单明细
from services.inbound.receiving_list.receiving_list_detail.api import router as router_receiving_list_detail

app.include_router(router_receiving_list_detail)


from services.inbound.receiving_list.receiving_record.api import router as router_receiving_record

app.include_router(router_receiving_record)


disable_installed_extensions_check() 


if __name__ == "__main__":
    uvicorn.run("main:app",port=8000, reload=True)
