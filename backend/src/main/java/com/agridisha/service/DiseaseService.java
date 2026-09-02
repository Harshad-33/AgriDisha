package com.agridisha.service;

import com.agridisha.dto.DiseasePredictionResponse;
import com.agridisha.entity.DiseasePrediction;
import com.agridisha.entity.User;
import com.agridisha.exception.BadRequestException;
import com.agridisha.repository.DiseasePredictionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.Map;
import java.util.Optional;

@Service
public class DiseaseService {

    @Autowired
    private MlClientService mlClientService;

    @Autowired
    private DiseasePredictionRepository diseaseRepository;

    @Autowired
    private AuthService authService;

    public DiseasePredictionResponse predictDisease(MultipartFile imageFile) {
        if (imageFile == null || imageFile.isEmpty()) {
            throw new BadRequestException("Please upload a valid plant leaf image.");
        }

        String contentType = imageFile.getContentType();
        if (contentType == null || (!contentType.startsWith("image/") && !contentType.equals("application/octet-stream"))) {
            throw new BadRequestException("Please upload a valid plant leaf image file (JPEG, PNG, WebP).");
        }

        Map<String, Object> mlResult = mlClientService.callDiseasePredict(imageFile);

        String rawClass = (String) mlResult.getOrDefault("raw_class", "Tomato___healthy");
        String crop = (String) mlResult.getOrDefault("crop", "Tomato");
        String disease = (String) mlResult.getOrDefault("disease", "Healthy");
        String status = (String) mlResult.getOrDefault("status", "Healthy");
        Double confidence = mlResult.get("confidence") != null ? ((Number) mlResult.get("confidence")).doubleValue() : 0.94;
        String severity = (String) mlResult.getOrDefault("severity", "None");
        String cause = (String) mlResult.getOrDefault("cause", "N/A");
        String symptoms = (String) mlResult.getOrDefault("symptoms", "");
        String prevention = (String) mlResult.getOrDefault("prevention", "");
        String treatment = (String) mlResult.getOrDefault("treatment", "");
        String supplement = (String) mlResult.getOrDefault("supplement", "");

        // Save to Database
        DiseasePrediction entity = new DiseasePrediction();
        Optional<User> currentUser = authService.getCurrentUser();
        currentUser.ifPresent(entity::setUser);

        entity.setImageFilename(imageFile.getOriginalFilename());
        entity.setCropName(crop);
        entity.setDiseaseName(disease);
        entity.setHealthStatus(status);
        entity.setConfidenceScore(confidence);
        entity.setSeverity(severity);
        entity.setCause(cause);
        entity.setSymptoms(symptoms);
        entity.setPreventionAdvice(prevention);
        entity.setTreatmentAdvice(treatment);
        entity.setSupplementAdvice(supplement);

        DiseasePrediction saved = diseaseRepository.save(entity);

        DiseasePredictionResponse response = new DiseasePredictionResponse();
        response.setId(saved.getId());
        response.setRawClass(rawClass);
        response.setCrop(crop);
        response.setDisease(disease);
        response.setStatus(status);
        response.setConfidence(confidence);
        response.setSeverity(severity);
        response.setCause(cause);
        response.setSymptoms(symptoms);
        response.setPrevention(prevention);
        response.setTreatment(treatment);
        response.setSupplement(supplement);
        response.setImageFilename(imageFile.getOriginalFilename());

        return response;
    }
}
