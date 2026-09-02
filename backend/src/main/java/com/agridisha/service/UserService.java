package com.agridisha.service;

import com.agridisha.dto.UserProfileDto;
import com.agridisha.entity.User;
import com.agridisha.exception.BadRequestException;
import com.agridisha.repository.CropPredictionRepository;
import com.agridisha.repository.DiseasePredictionRepository;
import com.agridisha.repository.FertilizerRecommendationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    private AuthService authService;

    @Autowired
    private CropPredictionRepository cropRepository;

    @Autowired
    private FertilizerRecommendationRepository fertilizerRepository;

    @Autowired
    private DiseasePredictionRepository diseaseRepository;

    public UserProfileDto getCurrentUserProfile() {
        User user = authService.getCurrentUser()
                .orElseThrow(() -> new BadRequestException("Not authenticated"));

        UserProfileDto dto = new UserProfileDto();
        dto.setId(user.getId());
        dto.setUsername(user.getUsername());
        dto.setEmail(user.getEmail());
        dto.setFullName(user.getFullName());
        dto.setLocation(user.getLocation());
        dto.setRole(user.getRole().name());
        dto.setCreatedAt(user.getCreatedAt());

        dto.setTotalCropPredictions(cropRepository.countByUser(user));
        dto.setTotalFertilizerRecommendations(fertilizerRepository.countByUser(user));
        dto.setTotalDiseasePredictions(diseaseRepository.countByUser(user));

        return dto;
    }
}
