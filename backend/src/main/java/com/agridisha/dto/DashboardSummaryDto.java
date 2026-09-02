package com.agridisha.dto;

import java.util.ArrayList;
import java.util.List;

public class DashboardSummaryDto {

    private long totalCropPredictions;
    private long totalFertilizerRecommendations;
    private long totalDiseasePredictions;
    private List<HistoryItemDto> recentActivities = new ArrayList<>();

    public DashboardSummaryDto() {
    }

    public DashboardSummaryDto(long totalCropPredictions, long totalFertilizerRecommendations, long totalDiseasePredictions, List<HistoryItemDto> recentActivities) {
        this.totalCropPredictions = totalCropPredictions;
        this.totalFertilizerRecommendations = totalFertilizerRecommendations;
        this.totalDiseasePredictions = totalDiseasePredictions;
        this.recentActivities = recentActivities;
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

    public List<HistoryItemDto> getRecentActivities() {
        return recentActivities;
    }

    public void setRecentActivities(List<HistoryItemDto> recentActivities) {
        this.recentActivities = recentActivities;
    }
}
