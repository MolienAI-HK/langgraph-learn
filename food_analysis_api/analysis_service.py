import cv2
import numpy as np
from typing import Dict
import random

class FoodAnalysisService:
    def __init__(self):
        # 定义食物颜色范围 (HSV格式)
        self.food_ranges = {
            "西红柿": ((0, 50, 50), (10, 255, 255)),  # 红色
            "土豆": ((20, 50, 50), (30, 255, 255)),   # 棕色/黄色
            "蔬菜": ((36, 25, 25), (86, 255, 255))    # 绿色
        }
        # 定义食物热量范围 (每100克)
        self.calorie_ranges = {
            "西红柿": (18, 22),
            "土豆": (77, 83),
            "蔬菜": (25, 50)
        }

    def analyze_image(self, image_path: str) -> Dict:
        """分析食物图片并返回营养信息"""
        # 1. 读取图片
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("无法读取图片文件")

        # 2. 转换到HSV颜色空间
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 3. 检测各种食物类型
        detected_foods = []
        for food_type, (lower, upper) in self.food_ranges.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            pixels = cv2.countNonZero(mask)
            if pixels > img.size * 0.2:  # 超过20%像素匹配
                detected_foods.append((food_type, pixels))
        
        # 4. 确定最可能的食物类型
        if detected_foods:
            # 选择像素匹配最多的食物类型
            food_type = max(detected_foods, key=lambda x: x[1])[0]
            # 生成随机热量值
            min_cal, max_cal = self.calorie_ranges[food_type]
            calories = random.randint(min_cal, max_cal)
        else:
            food_type = "其他食物"
            calories = random.randint(200, 400)  # 默认范围

        return {
            "food_type": food_type,
            "calories": calories,
            "is_healthy": food_type in ["西红柿", "蔬菜"]  # 西红柿和蔬菜视为健康
        }

    def compare_with_broccoli(self, calories: float) -> Dict:
        """与西兰花进行营养对比"""
        # 使用蔬菜热量范围中间值作为西兰花参考值
        broccoli_calories = sum(self.calorie_ranges["蔬菜"]) // 2
        ratio = calories / broccoli_calories
        
        return {
            "original_calories": calories,
            "broccoli_calories": broccoli_calories,
            "calorie_ratio": round(ratio, 2),
            "recommendation": "建议搭配西兰花食用" if ratio > 1.5 else "热量合理"
        }