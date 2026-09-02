import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DiseaseService } from '../../core/services/disease.service';
import { DiseasePredictionResponse } from '../../core/models/models';

@Component({
  selector: 'app-disease-detection',
  standalone: true,
  imports: [CommonModule],
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

  constructor(private diseaseService: DiseaseService) {}

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
    if (!this.selectedFile) {
      this.errorMessage = 'Please select or drop a plant leaf image first.';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.result = null;

    this.diseaseService.predictDisease(this.selectedFile).subscribe({
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
  }
}
