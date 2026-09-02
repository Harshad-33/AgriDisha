import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { FertilizerService } from '../../core/services/fertilizer.service';
import { FertilizerRecommendationResponse } from '../../core/models/models';

@Component({
  selector: 'app-fertilizer-recommendation',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './fertilizer-recommendation.component.html',
  styleUrls: ['./fertilizer-recommendation.component.css']
})
export class FertilizerRecommendationComponent {
  fertilizerForm: FormGroup;
  isLoading = false;
  result: FertilizerRecommendationResponse | null = null;
  errorMessage = '';

  availableCrops = [
    'Rice', 'Maize', 'Chickpea', 'Kidney Beans', 'Pigeon Peas',
    'Moth Beans', 'Mung Bean', 'Black Gram', 'Lentil', 'Pomegranate',
    'Banana', 'Mango', 'Grapes', 'Watermelon', 'Muskmelon',
    'Apple', 'Orange', 'Papaya', 'Coconut', 'Cotton',
    'Jute', 'Coffee', 'Wheat', 'Potato', 'Tomato'
  ];

  constructor(
    private fb: FormBuilder,
    private fertilizerService: FertilizerService
  ) {
    this.fertilizerForm = this.fb.group({
      cropName: ['Rice', [Validators.required]],
      nitrogen: [40, [Validators.required, Validators.min(0)]],
      phosphorous: [60, [Validators.required, Validators.min(0)]],
      potassium: [30, [Validators.required, Validators.min(0)]]
    });
  }

  loadSample(deficiency: 'N' | 'P' | 'K' | 'Balanced'): void {
    if (deficiency === 'N') {
      this.fertilizerForm.patchValue({ cropName: 'Rice', nitrogen: 25, phosphorous: 40, potassium: 40 });
    } else if (deficiency === 'P') {
      this.fertilizerForm.patchValue({ cropName: 'Chickpea', nitrogen: 40, phosphorous: 20, potassium: 80 });
    } else if (deficiency === 'K') {
      this.fertilizerForm.patchValue({ cropName: 'Banana', nitrogen: 100, phosphorous: 75, potassium: 20 });
    } else {
      this.fertilizerForm.patchValue({ cropName: 'Maize', nitrogen: 100, phosphorous: 50, potassium: 40 });
    }
  }

  onSubmit(): void {
    if (this.fertilizerForm.invalid) {
      this.fertilizerForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.result = null;

    this.fertilizerService.recommendFertilizer(this.fertilizerForm.value).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.result = response;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.error?.message || 'Failed to evaluate fertilizer requirements.';
      }
    });
  }

  reset(): void {
    this.result = null;
    this.errorMessage = '';
  }
}
