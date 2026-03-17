import logging
# 导入路由
from app.api.api_v1.api import api_router
from app.api.openapi.api import router as openapi_router
# 
from app.core.config import settings
from app.core.minio import init_minio
from app.startup.migarate import DatabaseMigrator
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Include routers
# 在其他文件中用APIRouter()来定义路由，然后在这里include进来
app.include_router(api_router, prefix=settings.API_V1_STR) # 业务API
app.include_router(openapi_router, prefix="/openapi") # 开放API

# 在启动时执行
@app.on_event("startup") 
async def startup_event(): # 启动事件，在应用启动时执行
    '''
    预先准备好数据库：
    初始化MinIO对象存储
    执行数据库迁移（alembic）
    '''
    # Initialize MinIO
    init_minio()
    # Run database migrations
    # 加载项目根目录下的 alembic.ini 配置文件，并绑定当前数据库的连接字符串
    migrator = DatabaseMigrator(settings.get_database_url) 
    migrator.run_migrations()


@app.get("/")
def root():
    return {"message": "Welcome to RAG Web UI API"}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
    }
