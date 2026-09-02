import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FertilizerRecommendationRequest, FertilizerRecommendationResponse } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class FertilizerService {
  private apiUrl = 'http://localhost:8080/api/fertilizer';

  constructor(private http: HttpClient) {}

  recommendFertilizer(data: FertilizerRecommendationRequest): Observable<FertilizerRecommendationResponse> {
    return this.http.post<FertilizerRecommendationResponse>(`${this.apiUrl}/recommend`, data);
  }
}
