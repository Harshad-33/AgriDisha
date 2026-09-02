package com.agridisha.dto;

import java.time.LocalDateTime;

public class UserProfileDto {

    private Long id;
    private String username;
    private String email;
    private String fullName;
    private String location;
    private String role;
    private LocalDateTime createdAt;
    private long totalCropPredictions;
    private long totalFertilizerRecommendations;
    private long totalDiseasePredictions;

    public UserProfileDto() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public long getTotalCropPredictions() {
        return totalCropPredictions;
    }

    public void setTotalCropPredictions(long totalCropPredictions) {
        this.totalCropPredictions = totalCropPredictions;
    }

    public long getTotalFertilizerRecommendations() {
        return totalFertilizerRecommendations;
    }

    public void setTotalFertilizerRecommendations(long totalFertilizerRecommendations) {
        this.totalFertilizerRecommendations = totalFertilizerRecommendations;
    }

    public long getTotalDiseasePredictions() {
        return totalDiseasePredictions;
    }

    public void setTotalDiseasePredictions(long totalDiseasePredictions) {
        this.totalDiseasePredictions = totalDiseasePredictions;
    }
}
