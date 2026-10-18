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

    @Column(length = 100)
    private String state;

    @Column(length = 100)
    private String district;

    @Column(name = "soil_color", length = 100)
    private String soilColor;

    @Column(name = "is_district_verified")
    private Boolean isDistrictVerified = false;

    @Column(name = "dataset_used", length = 150)
    private String datasetUsed;

    @Column(name = "reference_link", columnDefinition = "TEXT")
    private String referenceLink;

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

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getDistrict() {
        return district;
    }

    public void setDistrict(String district) {
        this.district = district;
    }

    public String getSoilColor() {
        return soilColor;
    }

    public void setSoilColor(String soilColor) {
        this.soilColor = soilColor;
    }

    public Boolean getIsDistrictVerified() {
        return isDistrictVerified;
    }

    public void setIsDistrictVerified(Boolean isDistrictVerified) {
        this.isDistrictVerified = isDistrictVerified;
    }

    public String getDatasetUsed() {
        return datasetUsed;
    }

    public void setDatasetUsed(String datasetUsed) {
        this.datasetUsed = datasetUsed;
    }

    public String getReferenceLink() {
        return referenceLink;
    }

    public void setReferenceLink(String referenceLink) {
        this.referenceLink = referenceLink;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
