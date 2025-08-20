import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000
})

export const createSession = async () => {
  try {
    const response = await api.post('/sessions')
    return response.data
  } catch (error) {
    console.error('创建会话失败:', error)
    throw error
  }
}

export const uploadImage = async (sessionId: string, imageFile: File) => {
  const formData = new FormData()
  formData.append('file', imageFile)
  
  try {
    const response = await api.post(`/sessions/${sessionId}/upload-image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  } catch (error) {
    console.error('上传图片失败:', error)
    throw error
  }
}

export const submitDietResponse = async (sessionId: string, isDieting: boolean) => {
  try {
    const response = await api.post(`/sessions/${sessionId}/diet-response`, {
      is_dieting: isDieting
    })
    return response.data
  } catch (error) {
    console.error('提交减肥回答失败:', error)
    throw error
  }
}

export const getHistory = async () => {
  try {
    const response = await api.get('/history')
    return response.data
  } catch (error) {
    console.error('获取历史记录失败:', error)
    throw error
  }
}