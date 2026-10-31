import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { DiseaseService } from '../../core/services/disease.service';
import { LocationService } from '../../core/services/location.service';
import { DiseasePredictionResponse } from '../../core/models/models';

@Component({
  selector: 'app-disease-detection',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './disease-detection.component.html',
  styleUrls: ['./disease-detection.component.css']
})
export class DiseaseDetectionComponent {
  selectedFile: File | null = null;
  imagePreview: string | ArrayBuffer | null = null;
  isDragging = false;
  isLoading = false;
  result: DiseasePredictionResponse | null = null;
  errorMessage = '';
  hasSubmitted = false;

  selectedState = '';
  selectedDistrict = '';
  states: string[] = [];
  districts: string[] = [];

  constructor(
    private diseaseService: DiseaseService,
    public locationService: LocationService
  ) {
    this.states = this.locationService.getStates();
    this.districts = [];
  }

  onStateChange(): void {
    this.selectedDistrict = '';
    if (this.selectedState) {
      this.districts = this.locationService.getDistricts(this.selectedState);
    } else {
      this.districts = [];
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.handleFile(input.files[0]);
    }
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;

    if (event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files[0]) {
      this.handleFile(event.dataTransfer.files[0]);
    }
  }

  private handleFile(file: File): void {
    if (!file.type.startsWith('image/')) {
      this.errorMessage = 'Please upload a valid plant leaf image (JPEG, PNG, WebP).';
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      this.errorMessage = 'Image size must be less than 10MB.';
      return;
    }

    this.selectedFile = file;
    this.errorMessage = '';
    this.result = null;

    const reader = new FileReader();
    reader.onload = () => {
      this.imagePreview = reader.result;
    };
    reader.readAsDataURL(file);
  }

  onSubmit(): void {
    this.hasSubmitted = true;

    if (!this.selectedState) {
      this.errorMessage = 'Please select a State before diagnosing the leaf.';
      return;
    }

    if (!this.selectedDistrict) {
      this.errorMessage = 'Please select a District before diagnosing the leaf.';
      return;
    }

    if (!this.selectedFile) {
      this.errorMessage = 'Please select or drop a plant leaf image first.';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.result = null;

    this.diseaseService.predictDisease(this.selectedFile, this.selectedState, this.selectedDistrict).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.result = response;
      },
      error: (err) => {
        this.isLoading = false;
        if (err.status === 503 || err.status === 500) {
          this.errorMessage = 'Prediction service is currently unavailable. Please try again.';
        } else {
          this.errorMessage = err.error?.message || 'Failed to detect plant disease.';
        }
      }
    });
  }

  reset(): void {
    this.selectedFile = null;
    this.imagePreview = null;
    this.result = null;
    this.errorMessage = '';
    this.hasSubmitted = false;
    this.selectedState = '';
    this.selectedDistrict = '';
    this.districts = [];
  }
}
