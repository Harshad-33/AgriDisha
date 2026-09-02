package com.agridisha.dto;

import java.time.LocalDateTime;

public class HistoryItemDto {

    private Long id;
    private String type; // CROP, FERTILIZER, DISEASE
    private String title;
    private String subtitle;
    private String detail;
    private String status;
    private Double confidence;
    private LocalDateTime createdAt;

    public HistoryItemDto() {
    }

    public HistoryItemDto(Long id, String type, String title, String subtitle, String detail, String status, Double confidence, LocalDateTime createdAt) {
        this.id = id;
        this.type = type;
        this.title = title;
        this.subtitle = subtitle;
        this.detail = detail;
        this.status = status;
        this.confidence = confidence;
        this.createdAt = createdAt;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getSubtitle() {
        return subtitle;
    }

    public void setSubtitle(String subtitle) {
        this.subtitle = subtitle;
    }

    public String getDetail() {
        return detail;
    }

    public void setDetail(String detail) {
        this.detail = detail;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
