import { useState, useEffect } from 'react'
import { Box, Typography, Paper, Table, TableBody, TableCell, TableRow, TableHead, CircularProgress } from '@mui/material'
import { getHistory } from '../services/api'
import type { NutritionData } from '../types'

export default function HistoryPage() {
  const [history, setHistory] = useState<NutritionData[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getHistory()
        setHistory(data)
      } catch (error) {
        console.error('获取历史记录失败:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [])

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        历史记录
      </Typography>
      
      {loading ? (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      ) : (
        <Paper sx={{ p: 3 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>食物名称</TableCell>
                <TableCell align="right">热量(kcal)</TableCell>
                <TableCell align="right">蛋白质(g)</TableCell>
                <TableCell align="right">碳水(g)</TableCell>
                <TableCell align="right">脂肪(g)</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {history.map((item, index) => (
                <TableRow key={index}>
                  <TableCell>{item.foodType}</TableCell>
                  <TableCell align="right">{item.calories}</TableCell>
                  <TableCell align="right">{item.protein}</TableCell>
                  <TableCell align="right">{item.carbs}</TableCell>
                  <TableCell align="right">{item.fat}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Box>
  )
}