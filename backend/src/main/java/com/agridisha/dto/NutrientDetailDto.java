package com.agridisha.dto;

public class NutrientDetailDto {

    private Double current;
    private Double ideal;
    private String status;

    public NutrientDetailDto() {
    }

    public NutrientDetailDto(Double current, Double ideal, String status) {
        this.current = current;
        this.ideal = ideal;
        this.status = status;
    }

    public Double getCurrent() {
        return current;
    }

    public void setCurrent(Double current) {
        this.current = current;
    }

    public Double getIdeal() {
        return ideal;
    }

    public void setIdeal(Double ideal) {
        this.ideal = ideal;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
