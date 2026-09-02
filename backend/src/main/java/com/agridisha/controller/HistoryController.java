package com.agridisha.controller;

import com.agridisha.dto.DashboardSummaryDto;
import com.agridisha.dto.HistoryItemDto;
import com.agridisha.service.HistoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/history")
public class HistoryController {

    @Autowired
    private HistoryService historyService;

    @GetMapping
    public ResponseEntity<List<HistoryItemDto>> getHistory() {
        List<HistoryItemDto> history = historyService.getUserHistory();
        return ResponseEntity.ok(history);
    }

    @GetMapping("/summary")
    public ResponseEntity<DashboardSummaryDto> getDashboardSummary() {
        DashboardSummaryDto summary = historyService.getDashboardSummary();
        return ResponseEntity.ok(summary);
    }
}
