# 食物营养分析系统

## 项目简介
基于FastAPI + React的全栈Web应用，提供食物图片营养分析功能。包含后端API服务和前端Web界面，用户可以上传晚餐照片，系统会分析食物热量并给出健康建议。

## 系统架构
- **后端API**: FastAPI开发的RESTful API服务
- **前端界面**: React + TypeScript + Vite构建的现代化Web应用
- **静态资源**: foods目录包含测试用食物图片

## 主要功能
- 用户会话管理
- 食物图片上传和分析
- 营养问答交互
- 历史记录查询
- 营养对比报告生成
- 响应式Web界面

## 后端API服务
使用项目根目录的 `run.ps1` 脚本一键启动服务：
```powershell
.\run.ps1
```

该脚本会自动：
1. 检查Python环境
2. 创建并激活虚拟环境
3. 安装项目依赖
4. 启动FastAPI服务器

服务启动后，访问 `http://localhost:8000/docs` 查看API文档。

### 前端Web应用
1. 进入前端项目目录
```bash
cd food-analysis-web
```

2. 安装依赖（使用pnpm）
```bash
pnpm install
```

3. 启动开发服务器
```bash
npm run dev
```

4. 访问前端应用
打开浏览器访问 `http://localhost:5173`

### 静态资源
项目包含 `foods/` 目录，内含测试用食物图片文件：
- 4651.jpg_wh860.jpg
- 4805.jpg_wh860.jpg  
- 34599220_184756238104_2.jpg
- fe1b-9ef71faea68f4f79f518f7bb7e9e6dc1.jpg

这些图片可用于前端开发和测试。
