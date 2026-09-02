package com.agridisha.dto;

import java.util.ArrayList;
import java.util.List;

public class CropRecommendationResponse {

    private Long id;
    private String recommendedCrop;
    private Double confidence;
    private String modelUsed;
    private String city;
    private Double temperature;
    private Double humidity;
    private Double nitrogen;
    private Double phosphorous;
    private Double potassium;
    private Double ph;
    private Double rainfall;
    private List<CropAlternativeDto> topAlternatives = new ArrayList<>();
    private String description;

    public CropRecommendationResponse() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getRecommendedCrop() {
        return recommendedCrop;
    }

    public void setRecommendedCrop(String recommendedCrop) {
        this.recommendedCrop = recommendedCrop;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }

    public String getModelUsed() {
        return modelUsed;
    }

    public void setModelUsed(String modelUsed) {
        this.modelUsed = modelUsed;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public Double getTemperature() {
        return temperature;
    }

    public void setTemperature(Double temperature) {
        this.temperature = temperature;
    }

    public Double getHumidity() {
        return humidity;
    }

    public void setHumidity(Double humidity) {
        this.humidity = humidity;
    }

    public Double getNitrogen() {
        return nitrogen;
    }

    public void setNitrogen(Double nitrogen) {
        this.nitrogen = nitrogen;
    }

    public Double getPhosphorous() {
        return phosphorous;
    }

    public void setPhosphorous(Double phosphorous) {
        this.phosphorous = phosphorous;
    }

    public Double getPotassium() {
        return potassium;
    }

    public void setPotassium(Double potassium) {
        this.potassium = potassium;
    }

    public Double getPh() {
        return ph;
    }

    public void setPh(Double ph) {
        this.ph = ph;
    }

    public Double getRainfall() {
        return rainfall;
    }

    public void setRainfall(Double rainfall) {
        this.rainfall = rainfall;
    }

    public List<CropAlternativeDto> getTopAlternatives() {
        return topAlternatives;
    }

    public void setTopAlternatives(List<CropAlternativeDto> topAlternatives) {
        this.topAlternatives = topAlternatives;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
