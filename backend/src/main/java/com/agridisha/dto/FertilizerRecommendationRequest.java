package com.agridisha.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class FertilizerRecommendationRequest {

    @NotBlank(message = "Crop name is required")
    private String cropName;

    @NotNull(message = "Nitrogen value is required")
    @DecimalMin(value = "0.0", message = "Nitrogen must be positive")
    private Double nitrogen;

    @NotNull(message = "Phosphorous value is required")
    @DecimalMin(value = "0.0", message = "Phosphorous must be positive")
    private Double phosphorous;

    @NotNull(message = "Potassium value is required")
    @DecimalMin(value = "0.0", message = "Potassium must be positive")
    private Double potassium;

    public FertilizerRecommendationRequest() {
    }

    public String getCropName() {
        return cropName;
    }

    public void setCropName(String cropName) {
        this.cropName = cropName;
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
}
