import { Component, OnInit, OnDestroy, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CropService } from '../../core/services/crop.service';
import { WeatherService } from '../../core/services/weather.service';
import { LocationService } from '../../core/services/location.service';
import { CropRecommendationResponse, WeatherResponse } from '../../core/models/models';

export interface CropSliderImage {
  src: string;
  alt: string;
}

@Component({
  selector: 'app-crop-recommendation',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './crop-recommendation.component.html',
  styleUrls: ['./crop-recommendation.component.css']
})
export class CropRecommendationComponent implements OnInit, OnDestroy {
  cropForm: FormGroup;
  isLoading = false;
  isWeatherLoading = false;
  weatherData: WeatherResponse | null = null;
  result: CropRecommendationResponse | null = null;
  errorMessage = '';
  weatherMessage = '';

  states: string[] = [];
  districts: string[] = [];

  // Hero Background Image Slider (crop_1.jpg and plant_2.jpg)
  currentSlide = 0;
  private autoSlideTimer: any = null;
  readonly slideIntervalMs = 4500; // 4.5s auto-transition
  private isBrowser: boolean;

  readonly sliderImages: CropSliderImage[] = [
    { src: 'Images/CropRecommendPage/crop_1.jpg', alt: 'AgriDisha Sustainable Farmland - Precision Crop Cultivation' },
    { src: 'Images/CropRecommendPage/plant_2.jpg', alt: 'AgriDisha Soil Health - Vibrant Green Crop Seedlings' }
  ];

  constructor(
    private fb: FormBuilder,
    private cropService: CropService,
    private weatherService: WeatherService,
    public locationService: LocationService,
    @Inject(PLATFORM_ID) platformId: object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
    this.states = this.locationService.getStates();
    this.districts = [];

    this.cropForm = this.fb.group({
      state: ['', [Validators.required]],
      district: ['', [Validators.required]],
      nitrogen: [null, [Validators.required, Validators.min(0), Validators.max(300)]],
      phosphorous: [null, [Validators.required, Validators.min(0), Validators.max(300)]],
      potassium: [null, [Validators.required, Validators.min(0), Validators.max(300)]],
      ph: [null, [Validators.required, Validators.min(3), Validators.max(10)]],
      rainfall: [null, [Validators.required, Validators.min(0), Validators.max(3000)]],
      city: ['', [Validators.required]],
      temperature: [null],
      humidity: [null]
    });
  }

  ngOnInit(): void {
    if (this.isBrowser) {
      this.startAutoSlide();
    }
  }

  ngOnDestroy(): void {
    this.stopAutoSlide();
  }

  startAutoSlide(): void {
    this.stopAutoSlide();
    if (!this.isBrowser) return;
    this.autoSlideTimer = setInterval(() => {
      this.nextSlide();
    }, this.slideIntervalMs);
  }

  stopAutoSlide(): void {
    if (this.autoSlideTimer) {
      clearInterval(this.autoSlideTimer);
      this.autoSlideTimer = null;
    }
  }

  nextSlide(): void {
    this.currentSlide = (this.currentSlide + 1) % this.sliderImages.length;
  }

  prevSlide(): void {
    this.currentSlide = (this.currentSlide - 1 + this.sliderImages.length) % this.sliderImages.length;
  }

  onUserNext(): void {
    this.nextSlide();
    this.startAutoSlide();
  }

  onUserPrev(): void {
    this.prevSlide();
    this.startAutoSlide();
  }

  goToSlide(index: number): void {
    this.currentSlide = index;
    this.startAutoSlide();
  }

  pauseSlider(): void {
    this.stopAutoSlide();
  }

  resumeSlider(): void {
    this.startAutoSlide();
  }

  onStateChange(): void {
    const state = this.cropForm.get('state')?.value;
    if (state) {
      this.districts = this.locationService.getDistricts(state);
      this.cropForm.patchValue({
        district: '',
        city: ''
      });
    } else {
      this.districts = [];
      this.cropForm.patchValue({
        district: '',
        city: ''
      });
    }
  }

  onDistrictChange(): void {
    const district = this.cropForm.get('district')?.value;
    if (district) {
      this.cropForm.patchValue({
        city: district
      });
    }
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
    if (type === 'solapur') {
      this.cropForm.setValue({
        state: 'Maharashtra',
        district: 'Solapur',
        nitrogen: 80,
        phosphorous: 40,
        potassium: 40,
        ph: 7.2,
        rainfall: 600,
        city: 'Solapur',
        temperature: 29.0,
        humidity: 55.0
      });
    } else if (type === 'pune') {
      this.cropForm.setValue({
        state: 'Maharashtra',
        district: 'Pune',
        nitrogen: 100,
        phosphorous: 50,
        potassium: 40,
        ph: 7.0,
        rainfall: 700,
        city: 'Pune',
        temperature: 25.0,
        humidity: 65.0
      });
    } else if (type === 'nagpur') {
      this.cropForm.setValue({
        state: 'Maharashtra',
        district: 'Nagpur',
        nitrogen: 85,
        phosphorous: 45,
        potassium: 40,
        ph: 6.8,
        rainfall: 950,
        city: 'Nagpur',
        temperature: 28.0,
        humidity: 68.0
      });
    } else if (type === 'cotton') {
      this.cropForm.setValue({
        state: 'Maharashtra',
        district: 'Yavatmal',
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
        state: 'Maharashtra',
        district: 'Latur',
        nitrogen: 30,
        phosphorous: 65,
        potassium: 35,
        ph: 6.8,
        rainfall: 850,
        city: 'Latur',
        temperature: 28.0,
        humidity: 68.0
      });
    } else if (type === 'rice') {
      this.cropForm.setValue({
        state: 'Maharashtra',
        district: 'Ratnagiri',
        nitrogen: 80,
        phosphorous: 40,
        potassium: 40,
        ph: 6.5,
        rainfall: 2200,
        city: 'Ratnagiri',
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
    this.weatherMessage = '';
    this.cropForm.reset({
      state: '',
      district: '',
      nitrogen: null,
      phosphorous: null,
      potassium: null,
      ph: null,
      rainfall: null,
      city: '',
      temperature: null,
      humidity: null
    });
    this.districts = [];
  }
}
