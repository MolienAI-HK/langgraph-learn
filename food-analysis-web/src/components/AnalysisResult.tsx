import { Box, Typography, Paper, Table, TableBody, TableCell, TableRow, Chip, Button } from '@mui/material'
import type { NutritionData } from '../types'

interface AnalysisResultProps {
  data: NutritionData
  onReset: () => void
}

export default function AnalysisResult({ data, onReset }: AnalysisResultProps) {
  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
        营养分析结果
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
          基本信息
        </Typography>
        <Table size="small">
          <TableBody>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold' }}>食物类型</TableCell>
              <TableCell>
                <Chip label={data.foodType} color="primary" />
              </TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold' }}>总热量</TableCell>
              <TableCell>{data.calories} kcal</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
          营养成分
        </Typography>
        <Table size="small">
          <TableBody>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold' }}>蛋白质</TableCell>
              <TableCell>{data.protein}g</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold' }}>碳水化合物</TableCell>
              <TableCell>{data.carbs}g</TableCell>
            </TableRow>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold' }}>脂肪</TableCell>
              <TableCell>{data.fat}g</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Paper>

      {data.vitamins && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
            维生素含量
          </Typography>
          <Table size="small">
            <TableBody>
              {Object.entries(data.vitamins).map(([name, value]) => (
                <TableRow key={name}>
                  <TableCell sx={{ fontWeight: 'bold' }}>{name}</TableCell>
                  <TableCell>{value as number}mg</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
          饮食建议
        </Typography>
        <Typography paragraph>{data.recommendation}</Typography>
        {data.comparison_table && (
          <>
            <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
              营养对比
            </Typography>
            {(() => {
              try {
                const comparisonData = JSON.parse(data.comparison_table.replace(/'/g, '"'));
                return (
                  <>
                    <Typography paragraph>
                      当前食物热量: {comparisonData.comparison_table?.food_calories ?? '未知'}kcal
                    </Typography>
                    <Typography paragraph>
                      相当于西兰花份数: {comparisonData.comparison_table?.broccoli_equivalent ?? '未知'}
                    </Typography>
                    <Typography paragraph>
                      营养密度: {comparisonData.comparison_table?.nutrient_density ?? '未知'}
                    </Typography>
                  </>
                );
              } catch (e) {
                console.error('解析comparison_table失败:', e);
                return (
                  <Typography color="error">
                    无法解析营养对比数据
                  </Typography>
                );
              }
            })()}
          </>
        )}
      </Paper>

      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          color="secondary"
          onClick={onReset}
        >
          重新分析
        </Button>
      </Box>
    </Box>
  )
}