package com.agridisha.controller;

import com.agridisha.dto.CropRecommendationRequest;
import com.agridisha.dto.CropRecommendationResponse;
import com.agridisha.service.CropService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/crop")
public class CropController {

    @Autowired
    private CropService cropService;

    @PostMapping("/recommend")
    public ResponseEntity<CropRecommendationResponse> recommendCrop(@Valid @RequestBody CropRecommendationRequest request) {
        CropRecommendationResponse response = cropService.recommendCrop(request);
        return ResponseEntity.ok(response);
    }
}
