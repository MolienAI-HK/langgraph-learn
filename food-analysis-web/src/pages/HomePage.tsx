import { Box, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <Box sx={{ textAlign: 'center', mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        食物营养分析系统
      </Typography>
      <Typography variant="body1" sx={{ mb: 4 }}>
        上传食物图片获取详细的营养分析报告
      </Typography>
      <Button 
        variant="contained" 
        size="large"
        onClick={() => navigate('/upload')}
      >
        开始分析
      </Button>
    </Box>
  );
}