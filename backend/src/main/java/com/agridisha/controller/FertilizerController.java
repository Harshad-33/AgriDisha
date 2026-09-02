package com.agridisha.controller;

import com.agridisha.dto.FertilizerRecommendationRequest;
import com.agridisha.dto.FertilizerRecommendationResponse;
import com.agridisha.service.FertilizerService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/fertilizer")
public class FertilizerController {

    @Autowired
    private FertilizerService fertilizerService;

    @PostMapping("/recommend")
    public ResponseEntity<FertilizerRecommendationResponse> recommendFertilizer(@Valid @RequestBody FertilizerRecommendationRequest request) {
        FertilizerRecommendationResponse response = fertilizerService.recommendFertilizer(request);
        return ResponseEntity.ok(response);
    }
}
