import { useState } from 'react'
import { Button, Box, Typography, CircularProgress } from '@mui/material'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'
import { createSession, uploadImage } from '../services/api'

interface ImageUploadProps {
  onUploadSuccess: (result: any) => void
  onUploadError?: (error: Error) => void
}

export default function ImageUpload({
  onUploadSuccess,
  onUploadError
}: ImageUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [sessionId, setSessionId] = useState<string>(() => {
    // 尝试从localStorage获取已有sessionId
    return localStorage.getItem('nutrition_sessionId') || ''
  })

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files?.[0]) {
      const file = event.target.files[0]
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return
    
    setIsUploading(true)
    try {
      // 如果没有有效sessionId则创建新会话
      let currentSessionId = sessionId
      if (!currentSessionId || currentSessionId.trim() === '') {
        const { session_id } = await createSession()
        currentSessionId = session_id
        setSessionId(currentSessionId)
        localStorage.setItem('nutrition_sessionId', currentSessionId)
      }
      
      // 上传图片
      const result = await uploadImage(currentSessionId, selectedFile)
      onUploadSuccess({
        ...result,
        session_id: currentSessionId
      })
    } catch (error) {
      console.error('上传失败:', error)
      onUploadError?.(error as Error)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        上传食物图片
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 2 }}>
        <Button
          variant="contained"
          component="label"
          startIcon={<CloudUploadIcon />}
          disabled={isUploading}
        >
          选择图片
          <input
            type="file"
            hidden
            accept="image/*"
            onChange={handleFileChange}
            disabled={isUploading}
          />
        </Button>
        
        {selectedFile && (
          <Typography variant="body1">
            已选择: {selectedFile.name}
          </Typography>
        )}
      </Box>

      {previewUrl && (
        <Box sx={{ mb: 2 }}>
          <img 
            src={previewUrl} 
            alt="预览" 
            style={{ maxWidth: '100%', maxHeight: '300px' }}
          />
        </Box>
      )}

      {selectedFile && (
        <Button
          variant="contained"
          color="primary"
          onClick={handleUpload}
          disabled={isUploading}
          fullWidth
          sx={{ mt: 2 }}
        >
          {isUploading ? (
            <>
              <CircularProgress size={24} sx={{ mr: 1 }} />
              分析中...
            </>
          ) : '开始分析'}
        </Button>
      )}
    </Box>
  )
}