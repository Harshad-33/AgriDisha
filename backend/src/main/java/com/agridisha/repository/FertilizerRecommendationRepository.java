package com.agridisha.repository;

import com.agridisha.entity.FertilizerRecommendation;
import com.agridisha.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FertilizerRecommendationRepository extends JpaRepository<FertilizerRecommendation, Long> {
    List<FertilizerRecommendation> findByUserOrderByCreatedAtDesc(User user);
    List<FertilizerRecommendation> findTop10ByUserOrderByCreatedAtDesc(User user);
    long countByUser(User user);
}
