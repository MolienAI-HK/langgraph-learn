import { useState } from 'react'
import { Box, Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from '@/pages/HomePage'
import HistoryPage from '@/pages/HistoryPage'
import NavBar from '@/components/NavBar'
import ImageUpload from '@/components/ImageUpload'
import DietQuestion from '@/components/DietQuestion'
import AnalysisResult from '@/components/AnalysisResult'
import type { NutritionData } from '@/types'

const theme = createTheme()

type AnalysisStep = 'upload' | 'diet-question' | 'result'

function App() {
  const [currentStep, setCurrentStep] = useState<AnalysisStep>('upload')
  const [analysisData, setAnalysisData] = useState<Partial<NutritionData>>({})
  const [sessionId, setSessionId] = useState('')

  const handleUploadSuccess = (result: any) => {
    setAnalysisData(prev => ({ ...prev, ...result }))
    setSessionId(result.session_id)
    setCurrentStep('diet-question')
  }

  const handleDietResponse = (result: any) => {
    setAnalysisData(prev => ({ ...prev, ...result }))
    setCurrentStep('result')
  }

  const resetAnalysis = () => {
    setCurrentStep('upload')
    setAnalysisData({})
    localStorage.removeItem('nutrition_sessionId')
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <NavBar />
        <Container maxWidth="lg">
          <Box sx={{ my: 4 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route
                path="/upload"
                element={
                  currentStep === 'upload' ? (
                    <ImageUpload onUploadSuccess={handleUploadSuccess} />
                  ) : currentStep === 'diet-question' ? (
                    <DietQuestion
                      sessionId={sessionId}
                      calories={analysisData.calories || 0}
                      onResponseSubmit={handleDietResponse}
                    />
                  ) : (
                    <AnalysisResult
                      data={analysisData as NutritionData}
                      onReset={resetAnalysis}
                    />
                  )
                }
              />
              <Route path="/history" element={<HistoryPage />} />
            </Routes>
          </Box>
        </Container>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
