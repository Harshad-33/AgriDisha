import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CropService } from '../../core/services/crop.service';
import { WeatherService } from '../../core/services/weather.service';
import { CropRecommendationResponse, WeatherResponse } from '../../core/models/models';

@Component({
  selector: 'app-crop-recommendation',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './crop-recommendation.component.html',
  styleUrls: ['./crop-recommendation.component.css']
})
export class CropRecommendationComponent {
  cropForm: FormGroup;
  isLoading = false;
  isWeatherLoading = false;
  weatherData: WeatherResponse | null = null;
  result: CropRecommendationResponse | null = null;
  errorMessage = '';
  weatherMessage = '';

  constructor(
    private fb: FormBuilder,
    private cropService: CropService,
    private weatherService: WeatherService
  ) {
    this.cropForm = this.fb.group({
      nitrogen: [110, [Validators.required, Validators.min(0), Validators.max(300)]],
      phosphorous: [45, [Validators.required, Validators.min(0), Validators.max(300)]],
      potassium: [25, [Validators.required, Validators.min(0), Validators.max(300)]],
      ph: [7.2, [Validators.required, Validators.min(3), Validators.max(10)]],
      rainfall: [850, [Validators.required, Validators.min(0), Validators.max(3000)]],
      city: ['Yavatmal', [Validators.required]],
      temperature: [29.5],
      humidity: [65.0]
    });
  }

  fetchWeather(): void {
    const city = this.cropForm.get('city')?.value;
    if (!city || city.trim() === '') {
      this.weatherMessage = 'Please enter a city name first.';
      return;
    }

    this.isWeatherLoading = true;
    this.weatherMessage = '';

    this.weatherService.getWeather(city.trim()).subscribe({
      next: (weather) => {
        this.isWeatherLoading = false;
        this.weatherData = weather;
        this.cropForm.patchValue({
          temperature: weather.temperature,
          humidity: weather.humidity
        });
        this.weatherMessage = `Weather fetched for ${weather.city}: ${weather.temperature}°C, ${weather.humidity}% humidity${weather.simulated ? ' (Simulated)' : ''}`;
      },
      error: () => {
        this.isWeatherLoading = false;
        this.weatherMessage = 'Unable to fetch weather data. Please enter temperature and humidity manually.';
      }
    });
  }

  loadPreset(type: string): void {
    if (type === 'cotton') {
      this.cropForm.setValue({
        nitrogen: 115,
        phosphorous: 45,
        potassium: 25,
        ph: 7.2,
        rainfall: 850,
        city: 'Yavatmal',
        temperature: 30.0,
        humidity: 62.0
      });
    } else if (type === 'soybean') {
      this.cropForm.setValue({
        nitrogen: 30,
        phosphorous: 65,
        potassium: 35,
        ph: 6.8,
        rainfall: 850,
        city: 'Yavatmal',
        temperature: 28.0,
        humidity: 68.0
      });
    } else if (type === 'sorghum') {
      this.cropForm.setValue({
        nitrogen: 85,
        phosphorous: 40,
        potassium: 40,
        ph: 7.0,
        rainfall: 750,
        city: 'Yavatmal',
        temperature: 29.0,
        humidity: 60.0
      });
    } else if (type === 'rice') {
      this.cropForm.setValue({
        nitrogen: 80,
        phosphorous: 40,
        potassium: 40,
        ph: 6.5,
        rainfall: 2200,
        city: 'Mumbai',
        temperature: 28.5,
        humidity: 82.0
      });
    }
  }

  loadSampleData(): void {
    this.loadPreset('cotton');
  }

  onSubmit(): void {
    if (this.cropForm.invalid) {
      this.cropForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.result = null;

    this.cropService.recommendCrop(this.cropForm.value).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.result = response;
      },
      error: (err) => {
        this.isLoading = false;
        if (err.status === 503 || err.status === 500) {
          this.errorMessage = 'Prediction service is currently unavailable. Please try again.';
        } else {
          this.errorMessage = err.error?.message || 'Failed to generate crop recommendation.';
        }
      }
    });
  }

  reset(): void {
    this.result = null;
    this.errorMessage = '';
  }
}
