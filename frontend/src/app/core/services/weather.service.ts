import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { WeatherResponse } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class WeatherService {
  private apiUrl = 'http://localhost:8080/api/weather';

  constructor(private http: HttpClient) {}

  getWeather(city: string): Observable<WeatherResponse> {
    return this.http.get<WeatherResponse>(`${this.apiUrl}/${encodeURIComponent(city)}`);
  }
}
