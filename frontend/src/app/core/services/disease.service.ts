import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DiseasePredictionResponse } from '../models/models';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DiseaseService {
  private apiUrl = `${environment.apiUrl}/disease`;

  constructor(private http: HttpClient) {}

  predictDisease(imageFile: File, state?: string, district?: string): Observable<DiseasePredictionResponse> {
    const formData = new FormData();
    formData.append('image', imageFile, imageFile.name);
    if (state) {
      formData.append('state', state);
    }
    if (district) {
      formData.append('district', district);
    }
    return this.http.post<DiseasePredictionResponse>(`${this.apiUrl}/predict`, formData);
  }
}
