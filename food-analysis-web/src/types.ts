export interface NutritionData {
  status: string
  session_id: string
  foodType: string
  calories: number
  protein?: number
  carbs?: number
  fat?: number
  vitamins?: Record<string, number>
  is_healthy: boolean
  is_dieting?: boolean
  recommendation: string
  comparison_table?: string
  comparison?: {
    food: string
    ratio: number
  }
}