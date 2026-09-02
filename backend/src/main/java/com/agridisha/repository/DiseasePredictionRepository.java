package com.agridisha.repository;

import com.agridisha.entity.DiseasePrediction;
import com.agridisha.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DiseasePredictionRepository extends JpaRepository<DiseasePrediction, Long> {
    List<DiseasePrediction> findByUserOrderByCreatedAtDesc(User user);
    List<DiseasePrediction> findTop10ByUserOrderByCreatedAtDesc(User user);
    long countByUser(User user);
}
