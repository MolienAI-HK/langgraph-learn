import unittest
import os
from unittest.mock import patch, MagicMock
from .langgraph_service import LangGraphNutritionService

class TestLangGraphNutritionService(unittest.TestCase):
    def setUp(self):
        self.service = LangGraphNutritionService()
        self.test_image = "test_image.jpg"
        
    @patch('food_analysis_api.langgraph_service.FoodAnalysisService')
    def test_image_analysis_flow(self, mock_analysis):
        # 设置模拟返回值
        mock_service = mock_analysis.return_value
        mock_service.analyze_image.return_value = {
            "food_type": "蔬菜",
            "calories": 50,
            "is_healthy": True
        }
        
        # 执行测试
        result = self.service.analyze_image_flow(self.test_image)
        
        # 验证结果
        self.assertEqual(result["food_type"], "蔬菜")
        self.assertEqual(result["calories"], 50)
        self.assertTrue(result["is_healthy"])
        self.assertTrue(result["analysis_complete"])

    @patch('food_analysis_api.langgraph_service.FoodAnalysisService')
    def test_advice_flow_dieting(self, mock_analysis):
        mock_service = mock_analysis.return_value
        mock_service.compare_with_broccoli.return_value = {
            "recommendation": "建议搭配西兰花食用",
            "calorie_ratio": 1.5
        }
        
        result = self.service.generate_advice_flow(300, True)
        self.assertIn("控制总热量摄入", result["advice"])

    @patch('food_analysis_api.langgraph_service.FoodAnalysisService')
    def test_advice_flow_normal(self, mock_analysis):
        mock_service = mock_analysis.return_value
        mock_service.compare_with_broccoli.return_value = {
            "recommendation": "热量合理",
            "calorie_ratio": 0.8
        }
        
        result = self.service.generate_advice_flow(200, False)
        self.assertIn("可适当增加摄入量", result["advice"])

if __name__ == '__main__':
    unittest.main()