package com.agridisha.dto;

public class NutrientLevelsDto {

    private NutrientDetailDto nitrogen;
    private NutrientDetailDto phosphorus;
    private NutrientDetailDto potassium;

    public NutrientLevelsDto() {
    }

    public NutrientLevelsDto(NutrientDetailDto nitrogen, NutrientDetailDto phosphorus, NutrientDetailDto potassium) {
        this.nitrogen = nitrogen;
        this.phosphorus = phosphorus;
        this.potassium = potassium;
    }

    public NutrientDetailDto getNitrogen() {
        return nitrogen;
    }

    public void setNitrogen(NutrientDetailDto nitrogen) {
        this.nitrogen = nitrogen;
    }

    public NutrientDetailDto getPhosphorus() {
        return phosphorus;
    }

    public void setPhosphorus(NutrientDetailDto phosphorus) {
        this.phosphorus = phosphorus;
    }

    public NutrientDetailDto getPotassium() {
        return potassium;
    }

    public void setPotassium(NutrientDetailDto potassium) {
        this.potassium = potassium;
    }
}
