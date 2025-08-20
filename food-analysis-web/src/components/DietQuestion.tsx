import { useState } from 'react'
import { Button, Box, Typography, Radio, RadioGroup, FormControlLabel, CircularProgress } from '@mui/material'
import { submitDietResponse } from '../services/api'

interface DietQuestionProps {
  sessionId: string
  calories: number
  onResponseSubmit: (result: any) => void
  onError?: (error: Error) => void
}

export default function DietQuestion({ 
  sessionId,
  calories,
  onResponseSubmit,
  onError
}: DietQuestionProps) {
  const [isDieting, setIsDieting] = useState<boolean | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async () => {
    if (isDieting === null) return
    
    setIsSubmitting(true)
    try {
      const result = await submitDietResponse(sessionId, isDieting)
      onResponseSubmit(result)
    } catch (error) {
      console.error('提交失败:', error)
      onError?.(error as Error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        饮食状态调查
      </Typography>
      <Typography variant="body1" gutterBottom>
        当前食物热量: {calories}kcal
      </Typography>
      
      <RadioGroup
        value={isDieting}
        onChange={(e) => setIsDieting(e.target.value === 'true')}
        sx={{ mb: 2 }}
      >
        <FormControlLabel value={true} control={<Radio />} label="我正在减肥" />
        <FormControlLabel value={false} control={<Radio />} label="我没有在减肥" />
      </RadioGroup>

      <Button
        variant="contained"
        color="primary"
        onClick={handleSubmit}
        disabled={isDieting === null || isSubmitting}
        fullWidth
      >
        {isSubmitting ? (
          <>
            <CircularProgress size={24} sx={{ mr: 1 }} />
            提交中...
          </>
        ) : '提交'}
      </Button>
    </Box>
  )
}