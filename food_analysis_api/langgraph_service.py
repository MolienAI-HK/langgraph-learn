from typing import Dict, Any
from langgraph.graph import Graph
from .analysis_service import FoodAnalysisService

class LangGraphNutritionService:
    def __init__(self):
        self.legacy_service = FoodAnalysisService()
        self.image_analysis_flow = self._build_image_analysis_flow()
        self.nutrition_advice_flow = self._build_nutrition_advice_flow()

    def _build_image_analysis_flow(self) -> Graph:
        """构建图片分析流程图"""
        builder = Graph()
        
        # 添加节点
        builder.add_node("preprocess_image", self._preprocess_image)
        builder.add_node("identify_food", self._identify_food)
        builder.add_node("estimate_calories", self._estimate_calories)
        builder.add_node("evaluate_nutrition", self._evaluate_nutrition)
        
        # 定义流程
        builder.add_edge("preprocess_image", "identify_food")
        builder.add_edge("identify_food", "estimate_calories")
        builder.add_edge("estimate_calories", "evaluate_nutrition")
        
        # 设置入口和结束节点
        builder.set_entry_point("preprocess_image")
        builder.set_finish_point("evaluate_nutrition")
        return builder.compile()

    def _build_nutrition_advice_flow(self) -> Graph:
        """构建营养建议流程图"""
        builder = Graph()
        
        builder.add_node("analyze_calories", self._analyze_calories)
        builder.add_node("evaluate_density", self._evaluate_density)
        builder.add_node("generate_advice", self._generate_advice)
        
        builder.add_edge("analyze_calories", "evaluate_density")
        builder.add_edge("evaluate_density", "generate_advice")
        
        # 设置入口和结束节点
        builder.set_entry_point("analyze_calories")
        builder.set_finish_point("generate_advice")
        return builder.compile()

    def analyze_image_flow(self, image_path: str) -> Dict[str, Any]:
        """执行图片分析流程"""
        return self.image_analysis_flow.invoke(image_path)

    def generate_advice_flow(self, calories: float, is_dieting: bool) -> Dict[str, Any]:
        """执行营养建议流程并生成对比表格"""
        result = self.nutrition_advice_flow.invoke({
            "calories": calories,
            "is_dieting": is_dieting
        })
        
        # 生成与西兰花的营养对比表格
        comparison = self.legacy_service.compare_with_broccoli(calories)
        result["comparison_table"] = {
            "food_calories": calories,
            "broccoli_equivalent": comparison["calorie_ratio"],
            "nutrient_density": "高" if comparison["calorie_ratio"] < 1.5 else "低"
        }
        
        # 根据减肥状态生成建议
        if is_dieting:
            result["recommendation"] = f"当前食物热量({calories}kcal)较高，相当于{comparison['calorie_ratio']}份西兰花。建议减少摄入量并搭配西兰花。"
        else:
            result["recommendation"] = f"当前食物营养密度不高({calories}kcal)，相当于{comparison['calorie_ratio']}份西兰花。建议增加西兰花等营养丰富的食物。"
            
        return result

    # 以下是各流程节点的具体实现
    def _preprocess_image(self, image_path: str) -> Dict:
        """图片预处理节点"""
        return {"image_path": image_path, "status": "preprocessed"}

    def _identify_food(self, state: Dict) -> Dict:
        """食物识别节点"""
        result = self.legacy_service.analyze_image(state["image_path"])
        return {**state, "food_type": result["food_type"]}

    def _estimate_calories(self, state: Dict) -> Dict:
        """热量估算节点"""
        result = self.legacy_service.analyze_image(state["image_path"])
        return {**state, "calories": result["calories"]}

    def _evaluate_nutrition(self, state: Dict) -> Dict:
        """营养评估节点"""
        return {
            **state,
            "is_healthy": state["food_type"] == "蔬菜",
            "analysis_complete": True
        }

    def _analyze_calories(self, state: Dict) -> Dict:
        """热量分析节点"""
        comparison = self.legacy_service.compare_with_broccoli(state["calories"])
        return {**state, "calorie_comparison": comparison}

    def _evaluate_density(self, state: Dict) -> Dict:
        """营养密度评估节点"""
        is_healthy = state["calorie_comparison"]["calorie_ratio"] < 2.0
        return {**state, "is_nutritious": is_healthy}

    def _generate_advice(self, state: Dict) -> Dict:
        """生成建议节点"""
        base = state["calorie_comparison"]["recommendation"]
        if state["is_dieting"]:
            return {"advice": f"{base} 并控制总热量摄入"}
        return {"advice": f"{base} 可适当增加摄入量"}