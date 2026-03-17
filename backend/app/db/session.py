from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.get_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db(): # 为每次请求创建一个 Session
    db = SessionLocal()
    try:
        yield db # 把 db 交给 FastAPI 的 Depends(get_db) 使用
    finally:
        db.close() 