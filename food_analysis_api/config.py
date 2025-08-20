from pathlib import Path

class Settings:
    # 数据库配置
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./food_analysis.db"
    
    # 静态文件配置
    STATIC_DIR: Path = Path(__file__).parent / "static"
    UPLOAD_DIR: Path = STATIC_DIR / "uploads"
    
    # 创建必要的目录
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()