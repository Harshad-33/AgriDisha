package com.agridisha.service;

import com.agridisha.exception.MlServiceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;

@Service
public class MlClientService {

    private static final Logger logger = LoggerFactory.getLogger(MlClientService.class);

    @Value("${agridisha.ml.service-url:http://localhost:8000}")
    private String mlServiceUrl;

    @Autowired
    private RestTemplate restTemplate;

    public Map<String, Object> callCropPredict(Map<String, Object> requestPayload) {
        String url = mlServiceUrl + "/api/ml/crop-predict";
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestPayload, headers);

            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                return (Map<String, Object>) response.getBody();
            }
            throw new MlServiceException("ML service returned unexpected status: " + response.getStatusCode());
        } catch (Exception ex) {
            logger.error("Failed to connect to Python ML service for crop prediction: {}", ex.getMessage());
            throw new MlServiceException("Prediction service is currently unavailable. Please try again.", ex);
        }
    }

    public Map<String, Object> callFertilizerRecommend(Map<String, Object> requestPayload) {
        String url = mlServiceUrl + "/api/ml/fertilizer-recommend";
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestPayload, headers);

            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                return (Map<String, Object>) response.getBody();
            }
            throw new MlServiceException("ML service returned unexpected status: " + response.getStatusCode());
        } catch (Exception ex) {
            logger.error("Failed to connect to Python ML service for fertilizer recommendation: {}", ex.getMessage());
            throw new MlServiceException("Prediction service is currently unavailable. Please try again.", ex);
        }
    }

    public Map<String, Object> callDiseasePredict(MultipartFile imageFile) {
        String url = mlServiceUrl + "/api/ml/disease-predict";
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.MULTIPART_FORM_DATA);

            ByteArrayResource resource = new ByteArrayResource(imageFile.getBytes()) {
                @Override
                public String getFilename() {
                    return imageFile.getOriginalFilename() != null ? imageFile.getOriginalFilename() : "leaf.jpg";
                }
            };

            MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
            body.add("image", resource);

            HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
            ResponseEntity<Map> response = restTemplate.postForEntity(url, requestEntity, Map.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                return (Map<String, Object>) response.getBody();
            }
            throw new MlServiceException("ML service returned unexpected status: " + response.getStatusCode());
        } catch (IOException ex) {
            throw new MlServiceException("Failed to read image file data.", ex);
        } catch (Exception ex) {
            logger.error("Failed to connect to Python ML service for disease detection: {}", ex.getMessage());
            throw new MlServiceException("Prediction service is currently unavailable. Please try again.", ex);
        }
    }
}
