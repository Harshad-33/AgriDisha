import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { FertilizerService } from '../../core/services/fertilizer.service';
import { LocationService } from '../../core/services/location.service';
import { FertilizerRecommendationResponse } from '../../core/models/models';

@Component({
  selector: 'app-fertilizer-recommendation',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './fertilizer-recommendation.component.html',
  styleUrls: ['./fertilizer-recommendation.component.css']
})
export class FertilizerRecommendationComponent {
  fertilizerForm: FormGroup;
  isLoading = false;
  result: FertilizerRecommendationResponse | null = null;
  errorMessage = '';

  states: string[] = [];
  districts: string[] = [];
  soilColors: string[] = [];

  availableCrops = [
    'Rice', 'Maize', 'Chickpea', 'Kidney Beans', 'Pigeon Peas',
    'Moth Beans', 'Mung Bean', 'Black Gram', 'Lentil', 'Pomegranate',
    'Banana', 'Mango', 'Grapes', 'Watermelon', 'Muskmelon',
    'Apple', 'Orange', 'Papaya', 'Coconut', 'Cotton',
    'Jute', 'Coffee', 'Wheat', 'Potato', 'Tomato', 'Sugarcane', 'Jowar'
  ];

  constructor(
    private fb: FormBuilder,
    private fertilizerService: FertilizerService,
    public locationService: LocationService
  ) {
    this.states = this.locationService.getStates();
    this.districts = this.locationService.getDistricts('Maharashtra');
    this.soilColors = this.locationService.getSoilColors();

    this.fertilizerForm = this.fb.group({
      cropName: ['Cotton', [Validators.required]],
      state: ['Maharashtra', [Validators.required]],
      district: ['Solapur', [Validators.required]],
      soilColor: ['Black Soil (Regur)', [Validators.required]],
      nitrogen: [80, [Validators.required, Validators.min(0)]],
      phosphorous: [40, [Validators.required, Validators.min(0)]],
      potassium: [40, [Validators.required, Validators.min(0)]]
    });
  }

  onStateChange(): void {
    const state = this.fertilizerForm.get('state')?.value;
    this.districts = this.locationService.getDistricts(state);
    const defaultDistrict = this.districts.length > 0 ? this.districts[0] : '';
    this.fertilizerForm.patchValue({
      district: defaultDistrict
    });
  }

  loadSample(deficiency: 'N' | 'P' | 'K' | 'Balanced' | 'Solapur' | 'Nagpur'): void {
    if (deficiency === 'Solapur') {
      this.fertilizerForm.patchValue({
        cropName: 'Sugarcane',
        state: 'Maharashtra',
        district: 'Solapur',
        soilColor: 'Black Soil (Regur)',
        nitrogen: 150,
        phosphorous: 60,
        potassium: 80
      });
    } else if (deficiency === 'Nagpur') {
      this.fertilizerForm.patchValue({
        cropName: 'Cotton',
        state: 'Maharashtra',
        district: 'Nagpur',
        soilColor: 'Black Soil (Regur)',
        nitrogen: 60,
        phosphorous: 30,
        potassium: 25
      });
    } else if (deficiency === 'N') {
      this.fertilizerForm.patchValue({ cropName: 'Rice', nitrogen: 25, phosphorous: 40, potassium: 40 });
    } else if (deficiency === 'P') {
      this.fertilizerForm.patchValue({ cropName: 'Chickpea', nitrogen: 40, phosphorous: 20, potassium: 80 });
    } else if (deficiency === 'K') {
      this.fertilizerForm.patchValue({ cropName: 'Banana', nitrogen: 100, phosphorous: 75, potassium: 20 });
    } else {
      this.fertilizerForm.patchValue({ cropName: 'Wheat', nitrogen: 100, phosphorous: 50, potassium: 40 });
    }
  }

  onSubmit(): void {
    if (this.fertilizerForm.invalid) {
      this.fertilizerForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const formValues = this.fertilizerForm.value;
    const requestData = {
      cropName: formValues.cropName,
      nitrogen: Number(formValues.nitrogen),
      phosphorous: Number(formValues.phosphorous),
      potassium: Number(formValues.potassium),
      state: formValues.state ? String(formValues.state).trim() : undefined,
      district: formValues.district ? String(formValues.district).trim() : undefined,
      soilColor: formValues.soilColor ? String(formValues.soilColor).trim() : undefined
    };

    this.fertilizerService.recommendFertilizer(requestData).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.result = response;
      },
      error: (error) => {
        this.isLoading = false;
        this.errorMessage = error.error?.message || 'Failed to evaluate fertilizer recommendation. Please try again.';
      }
    });
  }

  reset(): void {
    this.result = null;
    this.errorMessage = '';
  }
}
