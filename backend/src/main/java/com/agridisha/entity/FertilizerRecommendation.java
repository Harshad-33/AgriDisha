package com.agridisha.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "fertilizer_recommendations")
public class FertilizerRecommendation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    @Column(name = "crop_name", nullable = false, length = 100)
    private String cropName;

    @Column(nullable = false)
    private Double nitrogen;

    @Column(nullable = false)
    private Double phosphorous;

    @Column(nullable = false)
    private Double potassium;

    @Column(name = "soil_status", nullable = false, length = 100)
    private String soilStatus;

    @Column(name = "primary_recommendation", columnDefinition = "TEXT")
    private String primaryRecommendation;

    @Column(name = "chemical_fertilizers", columnDefinition = "TEXT")
    private String chemicalFertilizers;

    @Column(name = "organic_alternatives", columnDefinition = "TEXT")
    private String organicAlternatives;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public FertilizerRecommendation() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
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

    public String getSoilStatus() {
        return soilStatus;
    }

    public void setSoilStatus(String soilStatus) {
        this.soilStatus = soilStatus;
    }

    public String getPrimaryRecommendation() {
        return primaryRecommendation;
    }

    public void setPrimaryRecommendation(String primaryRecommendation) {
        this.primaryRecommendation = primaryRecommendation;
    }

    public String getChemicalFertilizers() {
        return chemicalFertilizers;
    }

    public void setChemicalFertilizers(String chemicalFertilizers) {
        this.chemicalFertilizers = chemicalFertilizers;
    }

    public String getOrganicAlternatives() {
        return organicAlternatives;
    }

    public void setOrganicAlternatives(String organicAlternatives) {
        this.organicAlternatives = organicAlternatives;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
