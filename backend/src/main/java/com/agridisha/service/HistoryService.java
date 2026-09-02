package com.agridisha.service;

import com.agridisha.dto.DashboardSummaryDto;
import com.agridisha.dto.HistoryItemDto;
import com.agridisha.entity.CropPrediction;
import com.agridisha.entity.DiseasePrediction;
import com.agridisha.entity.FertilizerRecommendation;
import com.agridisha.entity.User;
import com.agridisha.exception.BadRequestException;
import com.agridisha.repository.CropPredictionRepository;
import com.agridisha.repository.DiseasePredictionRepository;
import com.agridisha.repository.FertilizerRecommendationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class HistoryService {

    @Autowired
    private CropPredictionRepository cropRepository;

    @Autowired
    private FertilizerRecommendationRepository fertilizerRepository;

    @Autowired
    private DiseasePredictionRepository diseaseRepository;

    @Autowired
    private AuthService authService;

    public List<HistoryItemDto> getUserHistory() {
        User user = authService.getCurrentUser()
                .orElseThrow(() -> new BadRequestException("You must be logged in to view your prediction history."));

        List<HistoryItemDto> items = new ArrayList<>();

        // Crop predictions
        List<CropPrediction> crops = cropRepository.findByUserOrderByCreatedAtDesc(user);
        for (CropPrediction c : crops) {
            items.add(new HistoryItemDto(
                    c.getId(),
                    "CROP",
                    "Recommended Crop: " + c.getPredictedCrop(),
                    "N: " + c.getNitrogen() + ", P: " + c.getPhosphorous() + ", K: " + c.getPotassium() + (c.getCity() != null ? " (" + c.getCity() + ")" : ""),
                    "Rainfall: " + c.getRainfall() + "mm, pH: " + c.getPh() + ", Temp: " + c.getTemperature() + "°C",
                    "Completed",
                    c.getConfidenceScore(),
                    c.getCreatedAt()
            ));
        }

        // Fertilizer recommendations
        List<FertilizerRecommendation> fertilizers = fertilizerRepository.findByUserOrderByCreatedAtDesc(user);
        for (FertilizerRecommendation f : fertilizers) {
            items.add(new HistoryItemDto(
                    f.getId(),
                    "FERTILIZER",
                    "Fertilizer for " + f.getCropName(),
                    "Soil Status: " + f.getSoilStatus(),
                    f.getPrimaryRecommendation(),
                    f.getSoilStatus(),
                    null,
                    f.getCreatedAt()
            ));
        }

        // Disease predictions
        List<DiseasePrediction> diseases = diseaseRepository.findByUserOrderByCreatedAtDesc(user);
        for (DiseasePrediction d : diseases) {
            items.add(new HistoryItemDto(
                    d.getId(),
                    "DISEASE",
                    d.getCropName() + " - " + d.getDiseaseName(),
                    "Health Status: " + d.getHealthStatus() + (d.getSeverity() != null ? " (" + d.getSeverity() + " severity)" : ""),
                    d.getTreatmentAdvice(),
                    d.getHealthStatus(),
                    d.getConfidenceScore(),
                    d.getCreatedAt()
            ));
        }

        // Sort descending by created timestamp
        items.sort((a, b) -> b.getCreatedAt().compareTo(a.getCreatedAt()));
        return items;
    }

    public DashboardSummaryDto getDashboardSummary() {
        User user = authService.getCurrentUser()
                .orElseThrow(() -> new BadRequestException("You must be logged in to view dashboard statistics."));

        long cropCount = cropRepository.countByUser(user);
        long fertilizerCount = fertilizerRepository.countByUser(user);
        long diseaseCount = diseaseRepository.countByUser(user);

        List<HistoryItemDto> allHistory = getUserHistory();
        List<HistoryItemDto> recent = allHistory.size() > 5 ? allHistory.subList(0, 5) : allHistory;

        return new DashboardSummaryDto(cropCount, fertilizerCount, diseaseCount, recent);
    }
}
