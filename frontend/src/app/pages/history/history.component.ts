import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HistoryService } from '../../core/services/history.service';
import { HistoryItem } from '../../core/models/models';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {
  historyList: HistoryItem[] = [];
  filteredList: HistoryItem[] = [];
  activeFilter: 'ALL' | 'CROP' | 'FERTILIZER' | 'DISEASE' = 'ALL';
  isLoading = true;
  errorMessage = '';

  constructor(private historyService: HistoryService) {}

  ngOnInit(): void {
    this.fetchHistory();
  }

  fetchHistory(): void {
    this.isLoading = true;
    this.historyService.getHistory().subscribe({
      next: (data) => {
        this.historyList = data;
        this.applyFilter('ALL');
        this.isLoading = false;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = 'Could not load your farm prediction history.';
      }
    });
  }

  applyFilter(filter: 'ALL' | 'CROP' | 'FERTILIZER' | 'DISEASE'): void {
    this.activeFilter = filter;
    if (filter === 'ALL') {
      this.filteredList = [...this.historyList];
    } else {
      this.filteredList = this.historyList.filter(item => item.type === filter);
    }
  }
}
