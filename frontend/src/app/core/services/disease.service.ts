import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DiseasePredictionResponse } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class DiseaseService {
  private apiUrl = 'http://localhost:8080/api/disease';

  constructor(private http: HttpClient) {}

  predictDisease(imageFile: File): Observable<DiseasePredictionResponse> {
    const formData = new FormData();
    formData.append('image', imageFile, imageFile.name);
    return this.http.post<DiseasePredictionResponse>(`${this.apiUrl}/predict`, formData);
  }
}
