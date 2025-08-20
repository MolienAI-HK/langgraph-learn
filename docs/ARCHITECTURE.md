# 食物营养分析系统架构文档

## 1. 系统架构概述

```
┌───────────────────────────────────────────────────────┐
│                   客户端 (Web/App)                     │
└───────────────┬───────────────────────┬───────────────┘
                │                       │
┌───────────────▼───────┐ ┌─────────────▼───────────────┐
│      FastAPI 服务层    │ │        LangGraph 层         │
│                       │ │                             │
│ - 用户会话管理        │ │ - 营养分析流程编排          │
│ - 图片上传处理        │ │ - 多步骤决策逻辑           │
│ - API路由分发        │ │ - 状态管理                 │
└───────────────┬───────┘ └─────────────┬───────────────┘
                │                       │
┌───────────────▼───────────────────────▼───────────────┐
│                     数据服务层                         │
│                                                       │
│ - SQLite 数据库 (用户会话/分析记录)                   │
│ - 图片存储 (本地文件系统)                             │
└───────────────────────────────────────────────────────┘
```

## 2. LangGraph 应用说明

### 应用位置
LangGraph 被用于核心营养分析流程的编排，主要在两个场景：
1. 图片分析决策流程
2. 营养建议生成流程

### 使用原因
1. **复杂流程编排**：食物分析涉及多个步骤（图片识别、热量估算、营养评估），LangGraph 提供了清晰的流程编排能力
2. **状态管理**：用户交互过程需要维护多步状态（上传→分析→问答→建议），LangGraph 的状态机特性非常适合
3. **灵活性**：当需要添加新的分析步骤或调整流程时，LangGraph 的图结构使修改更加容易
4. **可观测性**：LangGraph 提供了流程可视化工具，便于调试和优化分析流程

## 3. 关键组件说明

### 3.1 FastAPI 服务层
- 处理HTTP请求/响应
- 用户认证和会话管理
- 静态文件服务
- API路由分发

### 3.2 LangGraph 流程层
```python
# 实际实现流程
class LangGraphNutritionService:
    def _build_image_analysis_flow(self) -> Graph:
        builder = Graph()
        builder.add_node("preprocess_image", self._preprocess_image)
        builder.add_node("identify_food", self._identify_food)
        builder.add_node("estimate_calories", self._estimate_calories)
        builder.add_node("evaluate_nutrition", self._evaluate_nutrition)
        builder.add_edge("preprocess_image", "identify_food")
        builder.add_edge("identify_food", "estimate_calories")
        builder.add_edge("estimate_calories", "evaluate_nutrition")
        return builder.compile()

    def _build_nutrition_advice_flow(self) -> Graph:
        builder = Graph()
        builder.add_node("analyze_calories", self._analyze_calories)
        builder.add_node("evaluate_density", self._evaluate_density)
        builder.add_node("generate_advice", self._generate_advice)
        builder.add_edge("analyze_calories", "evaluate_density")
        builder.add_edge("evaluate_density", "generate_advice")
        return builder.compile()
```

### 3.3 数据服务层
- SQLite 数据库存储用户会话和分析记录
- 本地文件系统存储上传的图片
- 数据模型包括：
  - UserSession
  - FoodAnalysis
  - NutritionComparison

## 4. 典型请求流程

1. 客户端创建会话 → FastAPI
2. 上传图片 → FastAPI → 存储到本地
3. 触发分析 → LangGraph 编排分析流程
   - 图片分析 → 热量估算 → 营养评估
4. 返回建议 → FastAPI 格式化为API响应
5. 客户端查询历史 → FastAPI 从数据库获取