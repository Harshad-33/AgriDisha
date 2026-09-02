package com.agridisha.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "disease_predictions")
public class DiseasePrediction {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    @Column(name = "image_filename", length = 255)
    private String imageFilename;

    @Column(name = "crop_name", nullable = false, length = 100)
    private String cropName;

    @Column(name = "disease_name", nullable = false, length = 150)
    private String diseaseName;

    @Column(name = "health_status", nullable = false, length = 50)
    private String healthStatus;

    @Column(name = "confidence_score")
    private Double confidenceScore;

    @Column(length = 50)
    private String severity;

    @Column(name = "cause", columnDefinition = "TEXT")
    private String cause;

    @Column(name = "symptoms", columnDefinition = "TEXT")
    private String symptoms;

    @Column(name = "prevention_advice", columnDefinition = "TEXT")
    private String preventionAdvice;

    @Column(name = "treatment_advice", columnDefinition = "TEXT")
    private String treatmentAdvice;

    @Column(name = "supplement_advice", columnDefinition = "TEXT")
    private String supplementAdvice;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public DiseasePrediction() {
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

    public String getImageFilename() {
        return imageFilename;
    }

    public void setImageFilename(String imageFilename) {
        this.imageFilename = imageFilename;
    }

    public String getCropName() {
        return cropName;
    }

    public void setCropName(String cropName) {
        this.cropName = cropName;
    }

    public String getDiseaseName() {
        return diseaseName;
    }

    public void setDiseaseName(String diseaseName) {
        this.diseaseName = diseaseName;
    }

    public String getHealthStatus() {
        return healthStatus;
    }

    public void setHealthStatus(String healthStatus) {
        this.healthStatus = healthStatus;
    }

    public Double getConfidenceScore() {
        return confidenceScore;
    }

    public void setConfidenceScore(Double confidenceScore) {
        this.confidenceScore = confidenceScore;
    }

    public String getSeverity() {
        return severity;
    }

    public void setSeverity(String severity) {
        this.severity = severity;
    }

    public String getCause() {
        return cause;
    }

    public void setCause(String cause) {
        this.cause = cause;
    }

    public String getSymptoms() {
        return symptoms;
    }

    public void setSymptoms(String symptoms) {
        this.symptoms = symptoms;
    }

    public String getPreventionAdvice() {
        return preventionAdvice;
    }

    public void setPreventionAdvice(String preventionAdvice) {
        this.preventionAdvice = preventionAdvice;
    }

    public String getTreatmentAdvice() {
        return treatmentAdvice;
    }

    public void setTreatmentAdvice(String treatmentAdvice) {
        this.treatmentAdvice = treatmentAdvice;
    }

    public String getSupplementAdvice() {
        return supplementAdvice;
    }

    public void setSupplementAdvice(String supplementAdvice) {
        this.supplementAdvice = supplementAdvice;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
