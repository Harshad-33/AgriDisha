import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FertilizerRecommendationRequest, FertilizerRecommendationResponse } from '../models/models';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class FertilizerService {
  private apiUrl = `${environment.apiUrl}/fertilizer`;

  constructor(private http: HttpClient) {}

  recommendFertilizer(data: FertilizerRecommendationRequest): Observable<FertilizerRecommendationResponse> {
    return this.http.post<FertilizerRecommendationResponse>(`${this.apiUrl}/recommend`, data);
  }
}
