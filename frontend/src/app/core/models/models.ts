export interface User {
  id: number;
  username: string;
  email: string;
  fullName: string;
  location: string;
  role: string;
}

export interface AuthResponse {
  token: string;
  type: string;
  id: number;
  username: string;
  email: string;
  fullName: string;
  role: string;
}

export interface WeatherResponse {
  city: string;
  temperature: number;
  humidity: number;
  description: string;
  icon: string;
  simulated: boolean;
}

export interface CropAlternative {
  crop: string;
  probability: number;
}

export interface CropRecommendationRequest {
  nitrogen: number;
  phosphorous: number;
  potassium: number;
  ph: number;
  rainfall: number;
  city?: string;
  temperature?: number;
  humidity?: number;
}

export interface CropRecommendationResponse {
  id: number;
  recommendedCrop: string;
  confidence: number;
  modelUsed: string;
  city: string;
  temperature: number;
  humidity: number;
  nitrogen: number;
  phosphorous: number;
  potassium: number;
  ph: number;
  rainfall: number;
  topAlternatives: CropAlternative[];
  description: string;
}

export interface FertilizerRecommendationRequest {
  cropName: string;
  nitrogen: number;
  phosphorous: number;
  potassium: number;
}

export interface NutrientDetail {
  current: number;
  ideal: number;
  status: string;
}

export interface NutrientLevels {
  nitrogen: NutrientDetail;
  phosphorus: NutrientDetail;
  potassium: NutrientDetail;
}

export interface FertilizerRecommendationResponse {
  id: number;
  crop: string;
  soilStatus: string;
  nitrogen: number;
  phosphorous: number;
  potassium: number;
  nutrientLevels: NutrientLevels;
  evaluations: string[];
  chemicalFertilizers: string[];
  organicAlternatives: string[];
  recommendations: string[];
  primaryRecommendation: string;
}

export interface DiseasePredictionResponse {
  id: number;
  rawClass: string;
  crop: string;
  disease: string;
  status: string;
  confidence: number;
  severity: string;
  cause: string;
  symptoms: string;
  prevention: string;
  treatment: string;
  supplement: string;
  imageFilename: string;
}

export interface HistoryItem {
  id: number;
  type: 'CROP' | 'FERTILIZER' | 'DISEASE';
  title: string;
  subtitle: string;
  detail: string;
  status: string;
  confidence?: number;
  createdAt: string;
}

export interface DashboardSummary {
  totalCropPredictions: number;
  totalFertilizerRecommendations: number;
  totalDiseasePredictions: number;
  recentActivities: HistoryItem[];
}

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  fullName: string;
  location: string;
  role: string;
  createdAt: string;
  totalCropPredictions: number;
  totalFertilizerRecommendations: number;
  totalDiseasePredictions: number;
}
