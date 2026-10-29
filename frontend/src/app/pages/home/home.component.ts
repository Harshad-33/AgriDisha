import { Component, OnInit, OnDestroy, Inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

export interface SliderImage {
  src: string;
  alt: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, OnDestroy {
  currentSlide = 0;
  private autoSlideTimer: any = null;
  readonly slideIntervalMs = 4500; // 4.5s auto-transition
  private isBrowser: boolean;

  // Dedicated 5 agricultural images exclusively for the homepage slider
  readonly sliderImages: SliderImage[] = [
    { src: 'Images/HomePage/home_1.jpg', alt: 'AgriDisha Farm Landscape - Sustainable Crop Cultivation' },
    { src: 'Images/HomePage/home_2.jpg', alt: 'AgriDisha Precision Agriculture - Rural Farmland Ecosystem' },
    { src: 'Images/HomePage/home_3.jpg', alt: 'AgriDisha Crop Health - Vibrant Green Crop Fields' },
    { src: 'Images/HomePage/home_4.jpg', alt: 'AgriDisha Golden Harvest - Cereal and Grain Production' },
    { src: 'Images/HomePage/home_5.jpg', alt: 'AgriDisha Smart Farming - Scenic Agricultural Panorama' }
  ];

  constructor(
    public authService: AuthService,
    @Inject(PLATFORM_ID) platformId: object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
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
    this.startAutoSlide(); // Reset interval timer upon manual navigation
  }

  onUserPrev(): void {
    this.prevSlide();
    this.startAutoSlide(); // Reset interval timer upon manual navigation
  }

  goToSlide(index: number): void {
    this.currentSlide = index;
    this.startAutoSlide(); // Reset interval timer upon manual dot selection
  }

  pauseSlider(): void {
    this.stopAutoSlide();
  }

  resumeSlider(): void {
    this.startAutoSlide();
  }
}
