from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from fastapi.responses import JSONResponse
from . import crud, models, schemas, analysis_service, langgraph_service
from .config import settings
from .database import SessionLocal, engine
import os

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="食物营养分析API")

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as exc:
        logger.error(f"Error processing request: {exc}")
        raise

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="food_analysis_api/static"), name="static")

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "食物营养分析服务运行中"}

@app.post("/sessions/", response_model=schemas.Session)
def create_session(db: Session = Depends(get_db)):
    return crud.create_session(db)

@app.get("/sessions/{session_id}", response_model=schemas.Session)
def read_session(session_id: str, db: Session = Depends(get_db)):
    db_session = crud.get_session(db, session_id=session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session

@app.post("/sessions/{session_id}/upload-image")
async def upload_image(
    session_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 验证会话存在
    db_session = crud.get_session(db, session_id=session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    # 验证文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    # 限制文件大小 (5MB)
    max_size = 5 * 1024 * 1024
    file.file.seek(0, 2)
    file_size = file.file.tell()
    if file_size > max_size:
        raise HTTPException(status_code=413, detail="File too large (max 5MB)")
    file.file.seek(0)

    try:
        # 保存上传文件
        file_path = os.path.join(settings.UPLOAD_DIR, f"{session_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # 使用LangGraph分析流程
        analyzer = langgraph_service.LangGraphNutritionService()
        analysis_result = analyzer.analyze_image_flow(file_path)
        
        # 创建分析记录
        analysis = schemas.AnalysisCreate(
            session_id=session_id,
            image_path=file_path,
            calories=analysis_result["calories"]
        )
        return crud.create_analysis(db, analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sessions/{session_id}/diet-response", response_model=schemas.Analysis)
def handle_diet_response(
    session_id: str,
    response: schemas.DietResponse,
    db: Session = Depends(get_db)
):
    # 获取最新的分析记录
    analyses = crud.get_analyses_by_session(db, session_id=session_id)
    if not analyses:
        raise HTTPException(status_code=404, detail="No analysis found for this session")
    
    # 更新分析记录
    latest_analysis = analyses[-1]
    latest_analysis.is_dieting = response.is_dieting

    # 使用LangGraph建议流程
    analyzer = langgraph_service.LangGraphNutritionService()
    comparison = analyzer.generate_advice_flow(
        latest_analysis.calories,
        response.is_dieting
    )
    
    if response.is_dieting:
        recommendation = f"当前食物热量({latest_analysis.calories}kcal)较高，相当于{comparison['comparison_table']['broccoli_equivalent']}份西兰花的热量。建议减少摄入量，搭配西兰花食用。"
    else:
        recommendation = f"当前食物营养密度不高({latest_analysis.calories}kcal)，相当于{comparison['comparison_table']['broccoli_equivalent']}份西兰花的热量。建议增加西兰花等营养丰富的食物。"

    latest_analysis.recommendation = recommendation
    latest_analysis.comparison_table = str(comparison)
    
    db.commit()
    db.refresh(latest_analysis)
    return latest_analysis

@app.post("/sessions/{session_id}/complete", response_model=schemas.Session)
def complete_session(session_id: str, db: Session = Depends(get_db)):
    return crud.complete_session(db, session_id=session_id)

if __name__ == "__main__":
    import uvicorn
@app.post("/analyze")
async def analyze_image(
    image: UploadFile = File(..., alias="image"),
    db: Session = Depends(get_db)
):
    try:
        # 创建新会话
        session = crud.create_session(db)
        
        # 验证上传目录存在
        if not os.path.exists(settings.UPLOAD_DIR):
            os.makedirs(settings.UPLOAD_DIR)
            logger.info(f"Created upload directory: {settings.UPLOAD_DIR}")
            
        # 复用现有的上传图片逻辑
        analysis_record = await upload_image(session.session_id, image, db)
        
        # 获取完整分析结果
        analyzer = langgraph_service.LangGraphNutritionService()
        file_path = analysis_record.image_path
        analysis_result = analyzer.analyze_image_flow(file_path)
        
        logger.info(f"Image analysis completed for session: {session.session_id}")
        return {
            "status": "success",
            "session_id": session.session_id,
            "calories": analysis_result.get("calories", 0),
            "food_type": analysis_result.get("food_type", "unknown"),
            "is_healthy": analysis_result.get("is_healthy", False),
            "recommendation": "建议搭配西兰花食用" if analysis_result.get("calories", 0) > 300 else "可以适量食用"
        }
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed: {str(e)}"
        )

@app.get("/history", response_model=List[schemas.Analysis])
def get_history(db: Session = Depends(get_db)):
    analyses = crud.get_all_analyses(db)
    return analyses

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11080)