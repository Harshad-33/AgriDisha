import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CropRecommendationRequest, CropRecommendationResponse } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class CropService {
  private apiUrl = 'http://localhost:8080/api/crop';

  constructor(private http: HttpClient) {}

  recommendCrop(data: CropRecommendationRequest): Observable<CropRecommendationResponse> {
    return this.http.post<CropRecommendationResponse>(`${this.apiUrl}/recommend`, data);
  }
}
