package com.agridisha.service;

import com.agridisha.dto.FertilizerRecommendationRequest;
import com.agridisha.dto.FertilizerRecommendationResponse;
import com.agridisha.dto.NutrientDetailDto;
import com.agridisha.dto.NutrientLevelsDto;
import com.agridisha.entity.FertilizerRecommendation;
import com.agridisha.entity.User;
import com.agridisha.repository.FertilizerRecommendationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class FertilizerService {

    @Autowired
    private MlClientService mlClientService;

    @Autowired
    private FertilizerRecommendationRepository fertilizerRepository;

    @Autowired
    private AuthService authService;

    public FertilizerRecommendationResponse recommendFertilizer(FertilizerRecommendationRequest request) {
        Map<String, Object> mlPayload = new HashMap<>();
        mlPayload.put("crop_name", request.getCropName());
        mlPayload.put("nitrogen", request.getNitrogen());
        mlPayload.put("phosphorous", request.getPhosphorous());
        mlPayload.put("potassium", request.getPotassium());

        Map<String, Object> mlResult = mlClientService.callFertilizerRecommend(mlPayload);

        String crop = (String) mlResult.getOrDefault("crop", request.getCropName());
        String soilStatus = (String) mlResult.getOrDefault("soil_status", "N: Optimal, P: Optimal, K: Optimal");
        String primaryRec = (String) mlResult.getOrDefault("primary_recommendation", "Soil nutrients are balanced.");

        List<String> evaluations = (List<String>) mlResult.getOrDefault("evaluations", new ArrayList<>());
        List<String> chemicalFertilizers = (List<String>) mlResult.getOrDefault("chemical_fertilizers", new ArrayList<>());
        List<String> organicAlternatives = (List<String>) mlResult.getOrDefault("organic_alternatives", new ArrayList<>());
        List<String> recommendations = (List<String>) mlResult.getOrDefault("recommendations", new ArrayList<>());

        // Parse Nutrient Levels
        NutrientLevelsDto levels = new NutrientLevelsDto();
        if (mlResult.get("nutrient_levels") instanceof Map) {
            Map<String, Object> nl = (Map<String, Object>) mlResult.get("nutrient_levels");
            levels.setNitrogen(parseNutrientDetail((Map<String, Object>) nl.get("nitrogen")));
            levels.setPhosphorus(parseNutrientDetail((Map<String, Object>) nl.get("phosphorus")));
            levels.setPotassium(parseNutrientDetail((Map<String, Object>) nl.get("potassium")));
        }

        // Save to Database
        FertilizerRecommendation entity = new FertilizerRecommendation();
        Optional<User> currentUser = authService.getCurrentUser();
        currentUser.ifPresent(entity::setUser);

        entity.setCropName(crop);
        entity.setNitrogen(request.getNitrogen());
        entity.setPhosphorous(request.getPhosphorous());
        entity.setPotassium(request.getPotassium());
        entity.setSoilStatus(soilStatus);
        entity.setPrimaryRecommendation(primaryRec);
        entity.setChemicalFertilizers(String.join("; ", chemicalFertilizers));
        entity.setOrganicAlternatives(String.join("; ", organicAlternatives));

        FertilizerRecommendation saved = fertilizerRepository.save(entity);

        FertilizerRecommendationResponse response = new FertilizerRecommendationResponse();
        response.setId(saved.getId());
        response.setCrop(crop);
        response.setSoilStatus(soilStatus);
        response.setNitrogen(request.getNitrogen());
        response.setPhosphorous(request.getPhosphorous());
        response.setPotassium(request.getPotassium());
        response.setNutrientLevels(levels);
        response.setEvaluations(evaluations);
        response.setChemicalFertilizers(chemicalFertilizers);
        response.setOrganicAlternatives(organicAlternatives);
        response.setRecommendations(recommendations);
        response.setPrimaryRecommendation(primaryRec);

        return response;
    }

    private NutrientDetailDto parseNutrientDetail(Map<String, Object> map) {
        if (map == null) return new NutrientDetailDto(0.0, 0.0, "Optimal");
        Double current = map.get("current") != null ? ((Number) map.get("current")).doubleValue() : 0.0;
        Double ideal = map.get("ideal") != null ? ((Number) map.get("ideal")).doubleValue() : 0.0;
        String status = (String) map.getOrDefault("status", "Optimal");
        return new NutrientDetailDto(current, ideal, status);
    }
}
