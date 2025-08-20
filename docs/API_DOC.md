# API详细文档

## 1. 会话管理

### 创建会话
- 路径: POST /sessions/
- 请求参数: 无
- 返回: 会话ID和创建时间

### 获取会话状态
- 路径: GET /sessions/{session_id}
- 请求参数: session_id
- 返回: 会话详细信息

## 2. 图片分析

### 上传图片
- 路径: POST /sessions/{session_id}/upload-image
- 请求参数: 
  - session_id: 路径参数
  - file: 图片文件
- 返回: 分析结果

## 3. 营养建议

### 提交饮食偏好
- 路径: POST /sessions/{session_id}/diet-response
- 请求参数:
  - is_dieting: 是否在减肥
- 返回: 个性化营养建议

## 4. 历史记录

### 查询历史
- 路径: GET /sessions/{session_id}/history
- 请求参数: session_id
- 返回: 所有分析记录