package com.agridisha.controller;

import com.agridisha.dto.DiseasePredictionResponse;
import com.agridisha.service.DiseaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/disease")
public class DiseaseController {

    @Autowired
    private DiseaseService diseaseService;

    @PostMapping(value = "/predict", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<DiseasePredictionResponse> predictDisease(@RequestParam("image") MultipartFile image) {
        DiseasePredictionResponse response = diseaseService.predictDisease(image);
        return ResponseEntity.ok(response);
    }
}
