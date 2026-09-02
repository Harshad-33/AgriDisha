package com.agridisha.dto;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;

public class CropRecommendationRequest {

    @NotNull(message = "Nitrogen value is required")
    @DecimalMin(value = "0.0", message = "Nitrogen must be positive")
    @DecimalMax(value = "300.0", message = "Nitrogen value is unrealistically high")
    private Double nitrogen;

    @NotNull(message = "Phosphorous value is required")
    @DecimalMin(value = "0.0", message = "Phosphorous must be positive")
    @DecimalMax(value = "300.0", message = "Phosphorous value is unrealistically high")
    private Double phosphorous;

    @NotNull(message = "Potassium value is required")
    @DecimalMin(value = "0.0", message = "Potassium must be positive")
    @DecimalMax(value = "300.0", message = "Potassium value is unrealistically high")
    private Double potassium;

    @NotNull(message = "pH level is required")
    @DecimalMin(value = "0.0", message = "pH must be at least 0.0")
    @DecimalMax(value = "14.0", message = "pH cannot exceed 14.0")
    private Double ph;

    @NotNull(message = "Rainfall value is required")
    @DecimalMin(value = "0.0", message = "Rainfall must be positive")
    @DecimalMax(value = "5000.0", message = "Rainfall value is unrealistically high")
    private Double rainfall;

    private String city;
    private Double temperature;
    private Double humidity;

    public CropRecommendationRequest() {
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
}
