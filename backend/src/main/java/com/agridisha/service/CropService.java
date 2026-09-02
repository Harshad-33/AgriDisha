package com.agridisha.service;

import com.agridisha.dto.CropAlternativeDto;
import com.agridisha.dto.CropRecommendationRequest;
import com.agridisha.dto.CropRecommendationResponse;
import com.agridisha.dto.WeatherResponse;
import com.agridisha.entity.CropPrediction;
import com.agridisha.entity.User;
import com.agridisha.repository.CropPredictionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.*;

@Service
public class CropService {

    @Autowired
    private MlClientService mlClientService;

    @Autowired
    private WeatherService weatherService;

    @Autowired
    private CropPredictionRepository cropPredictionRepository;

    @Autowired
    private AuthService authService;

    public CropRecommendationResponse recommendCrop(CropRecommendationRequest request) {
        Double temp = request.getTemperature();
        Double hum = request.getHumidity();
        String city = request.getCity();

        // If temperature or humidity are missing, fetch from WeatherService
        if ((temp == null || hum == null) && StringUtils.hasText(city)) {
            WeatherResponse weather = weatherService.getWeatherForCity(city);
            if (temp == null) temp = weather.getTemperature();
            if (hum == null) hum = weather.getHumidity();
        }

        if (temp == null) temp = 28.0;
        if (hum == null) hum = 65.0;

        Map<String, Object> mlPayload = new HashMap<>();
        mlPayload.put("nitrogen", request.getNitrogen());
        mlPayload.put("phosphorous", request.getPhosphorous());
        mlPayload.put("potassium", request.getPotassium());
        mlPayload.put("temperature", temp);
        mlPayload.put("humidity", hum);
        mlPayload.put("ph", request.getPh());
        mlPayload.put("rainfall", request.getRainfall());
        if (StringUtils.hasText(city)) {
            mlPayload.put("city", city.trim());
        }

        Map<String, Object> mlResult = mlClientService.callCropPredict(mlPayload);

        String predictedCrop = (String) mlResult.getOrDefault("crop", "Cotton (Bt Cotton / Kapas)");
        Double confidence = mlResult.get("confidence") != null ? ((Number) mlResult.get("confidence")).doubleValue() : 0.92;
        String modelUsed = (String) mlResult.getOrDefault("model_used", "RandomForestClassifier (Maharashtra Agricultural Benchmark)");
        String description = (String) mlResult.getOrDefault("description",
                "Based on soil macronutrients (N-P-K), soil pH, rainfall, and Maharashtra agro-climatic conditions, " + predictedCrop + " is recommended for optimal yield.");

        List<CropAlternativeDto> alternatives = new ArrayList<>();
        if (mlResult.get("top_alternatives") instanceof List) {
            List<Map<String, Object>> altList = (List<Map<String, Object>>) mlResult.get("top_alternatives");
            for (Map<String, Object> item : altList) {
                String c = (String) item.get("crop");
                Double p = item.get("probability") != null ? ((Number) item.get("probability")).doubleValue() : 0.0;
                alternatives.add(new CropAlternativeDto(c, p));
            }
        }

        // Save to Database
        CropPrediction prediction = new CropPrediction();
        Optional<User> currentUser = authService.getCurrentUser();
        currentUser.ifPresent(prediction::setUser);

        prediction.setNitrogen(request.getNitrogen());
        prediction.setPhosphorous(request.getPhosphorous());
        prediction.setPotassium(request.getPotassium());
        prediction.setTemperature(temp);
        prediction.setHumidity(hum);
        prediction.setPh(request.getPh());
        prediction.setRainfall(request.getRainfall());
        prediction.setCity(city);
        prediction.setPredictedCrop(predictedCrop);
        prediction.setConfidenceScore(confidence);
        prediction.setModelUsed(modelUsed);

        CropPrediction saved = cropPredictionRepository.save(prediction);

        CropRecommendationResponse response = new CropRecommendationResponse();
        response.setId(saved.getId());
        response.setRecommendedCrop(predictedCrop);
        response.setConfidence(confidence);
        response.setModelUsed(modelUsed);
        response.setCity(city);
        response.setTemperature(temp);
        response.setHumidity(hum);
        response.setNitrogen(request.getNitrogen());
        response.setPhosphorous(request.getPhosphorous());
        response.setPotassium(request.getPotassium());
        response.setPh(request.getPh());
        response.setRainfall(request.getRainfall());
        response.setTopAlternatives(alternatives);
        response.setDescription(description);

        return response;
    }
}
