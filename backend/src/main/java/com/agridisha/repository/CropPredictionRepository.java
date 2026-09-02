package com.agridisha.repository;

import com.agridisha.entity.CropPrediction;
import com.agridisha.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CropPredictionRepository extends JpaRepository<CropPrediction, Long> {
    List<CropPrediction> findByUserOrderByCreatedAtDesc(User user);
    List<CropPrediction> findTop10ByUserOrderByCreatedAtDesc(User user);
    long countByUser(User user);
}
