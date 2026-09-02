package com.agridisha.dto;

public class CropAlternativeDto {

    private String crop;
    private Double probability;

    public CropAlternativeDto() {
    }

    public CropAlternativeDto(String crop, Double probability) {
        this.crop = crop;
        this.probability = probability;
    }

    public String getCrop() {
        return crop;
    }

    public void setCrop(String crop) {
        this.crop = crop;
    }

    public Double getProbability() {
        return probability;
    }

    public void setProbability(Double probability) {
        this.probability = probability;
    }
}
