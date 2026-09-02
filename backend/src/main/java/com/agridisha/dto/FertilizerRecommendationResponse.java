package com.agridisha.dto;

import java.util.ArrayList;
import java.util.List;

public class FertilizerRecommendationResponse {

    private Long id;
    private String crop;
    private String soilStatus;
    private Double nitrogen;
    private Double phosphorous;
    private Double potassium;
    private NutrientLevelsDto nutrientLevels;
    private List<String> evaluations = new ArrayList<>();
    private List<String> chemicalFertilizers = new ArrayList<>();
    private List<String> organicAlternatives = new ArrayList<>();
    private List<String> recommendations = new ArrayList<>();
    private String primaryRecommendation;

    public FertilizerRecommendationResponse() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCrop() {
        return crop;
    }

    public void setCrop(String crop) {
        this.crop = crop;
    }

    public String getSoilStatus() {
        return soilStatus;
    }

    public void setSoilStatus(String soilStatus) {
        this.soilStatus = soilStatus;
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

    public NutrientLevelsDto getNutrientLevels() {
        return nutrientLevels;
    }

    public void setNutrientLevels(NutrientLevelsDto nutrientLevels) {
        this.nutrientLevels = nutrientLevels;
    }

    public List<String> getEvaluations() {
        return evaluations;
    }

    public void setEvaluations(List<String> evaluations) {
        this.evaluations = evaluations;
    }

    public List<String> getChemicalFertilizers() {
        return chemicalFertilizers;
    }

    public void setChemicalFertilizers(List<String> chemicalFertilizers) {
        this.chemicalFertilizers = chemicalFertilizers;
    }

    public List<String> getOrganicAlternatives() {
        return organicAlternatives;
    }

    public void setOrganicAlternatives(List<String> organicAlternatives) {
        this.organicAlternatives = organicAlternatives;
    }

    public List<String> getRecommendations() {
        return recommendations;
    }

    public void setRecommendations(List<String> recommendations) {
        this.recommendations = recommendations;
    }

    public String getPrimaryRecommendation() {
        return primaryRecommendation;
    }

    public void setPrimaryRecommendation(String primaryRecommendation) {
        this.primaryRecommendation = primaryRecommendation;
    }
}
