import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { DiseaseService } from '../../core/services/disease.service';
import { LocationService } from '../../core/services/location.service';
import { DiseasePredictionResponse } from '../../core/models/models';

export interface DiseaseDatasetInfo {
  datasetName: string;
  sourceOrg: string;
  cropsCovered: string;
  classesCount: string;
  imageRecords?: string;
  geoCoverage: string;
  licenceAttribution?: string;
  regionalFocus?: string;
}

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

  selectedState = 'Maharashtra';
  selectedDistrict = 'Solapur';
  states: string[] = [];
  districts: string[] = [];

  // Verified empirical disease datasets and regional agro-climatic pathology metadata
  private readonly stateDatasetMetadata: Record<string, DiseaseDatasetInfo> = {
    'Maharashtra': {
      datasetName: 'PlantVillage Disease Repository & Maharashtra SAU Pathology Protocols',
      sourceOrg: 'Penn State University / EPFL & Maharashtra State Agricultural Universities (MPKV Rahuri, PDKV Akola, VNMKV Parbhani, BSKKV Dapoli)',
      cropsCovered: '14 Core Agricultural Crops (Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato) & Regional Cash Crops',
      classesCount: '38 Verified Plant Pathology Classes',
      imageRecords: '54,306 Verified Agricultural Leaf Photographs',
      geoCoverage: 'Maharashtra (All 36 Districts across Vidarbha, Marathwada, Western Maharashtra, Khandesh, and Konkan)',
      licenceAttribution: 'Creative Commons CC0 1.0 Universal (Public Domain Dedication)',
      regionalFocus: 'Sugarcane, Cotton, Soybean, Pomegranate, Grapes, and Citrus Integrated Pest Management'
    },
    'Punjab': {
      datasetName: 'ICAR Crop Disease & Insect-Pest Image Dataset / PlantVillage Benchmark',
      sourceOrg: 'DARE / ICAR (ICAR-IASRI, AIKosh National Platform ID: 2448fb9b) & Punjab Agricultural University (PAU Ludhiana)',
      cropsCovered: 'Rice, Maize, Potato, Tomato, Pepper, and 14 Standard Agricultural Crops',
      classesCount: '38 Core Plant Pathology Classes + 15 ICAR Specialized Rice & Maize Biotic Stress Classes',
      imageRecords: '54,306 Benchmark Photographs + 925.9 MB ICAR National Field Dataset (450 Multi-Zone Samples)',
      geoCoverage: 'Punjab (All 23 Districts across Majha, Doaba, and Malwa Agro-Climatic Zones)',
      licenceAttribution: 'ICAR Data Use License & Creative Commons CC0 1.0',
      regionalFocus: 'Bacterial Leaf Blight, Sheath Blight, False Smut, and Stem Borer Management under PAU Kharif & Rabi Bulletins'
    },
    'Telangana': {
      datasetName: 'Mendeley Rice Leaf Disease Classification Dataset & PlantVillage Benchmark',
      sourceOrg: 'Professor Jayashankar Telangana State Agricultural University (PJTSAU) & Mendeley Data (DOI: 10.17632/zfwkkdj6dk.1)',
      cropsCovered: 'Rice / Paddy, Tomato, Pepper, Maize, and 14 Horticultural Crops',
      classesCount: '38 Core Plant Pathology Classes + 4 Specialized Rice Disease Classes',
      imageRecords: '54,306 Benchmark Images + Verified Regional Field Image Archive',
      geoCoverage: 'Telangana (All 33 Districts across Northern, Central, and Southern Telangana Agro-Climatic Zones)',
      licenceAttribution: 'Creative Commons CC0 1.0 & Mendeley Data Open License',
      regionalFocus: 'Bacterial Leaf Blight, Fungal Blast, Brown Spot, and Rice Tungro Virus Protocols (PJTSAU RARS Jagtial / Warangal / Palem)'
    },
    'Andhra Pradesh': {
      datasetName: 'Krishna River Basin Chili Disease Dataset & PlantVillage Benchmark',
      sourceOrg: 'Acharya N.G. Ranga Agricultural University (ANGRAU RARS Lam, Guntur), Dr. YSRHU, & Mendeley Data (DOI: 10.17632/ymt8k9bjkn.3)',
      cropsCovered: 'Chili / Pepper, Tomato, Potato, Maize, and 14 Agricultural Crops',
      classesCount: '38 Core Plant Pathology Classes + 6 Krishna Basin Chili Foliar Classes',
      imageRecords: '54,306 Benchmark Images + Regional Multi-Field Image Archive',
      geoCoverage: 'Andhra Pradesh (All 26 Districts including Krishna Delta, Guntur Chili Belt, Godavari Basin, and Rayalaseema)',
      licenceAttribution: 'Creative Commons CC0 1.0 & Mendeley Open Research License',
      regionalFocus: 'Chili Leaf Curl Begomovirus, Bacterial Spot, Cercospora Spot, and Micronutrient Deficiency Protocols'
    },
    'Karnataka': {
      datasetName: 'Arecanut Disease Detection Dataset & PlantVillage Benchmark',
      sourceOrg: 'KSNUAHS Shivamogga, CPCRI Regional Station Vittal, UAS Dharwad, UAS Bangalore, and Research Archive',
      cropsCovered: 'Arecanut, Pepper/Chili, Tomato, Potato, Maize, and 14 Agricultural Crops',
      classesCount: '38 Core Plant Pathology Classes + 6 Arecanut Plantation Disease & Frond Health Classes',
      imageRecords: '54,306 Benchmark Images + 301 Verified Arecanut Plantation Samples',
      geoCoverage: 'Karnataka (All 31 Districts across Malnad, Coastal, Northern Dry, and Southern Transition Zones)',
      licenceAttribution: 'Creative Commons CC0 1.0 & Open Research Attribution',
      regionalFocus: 'Arecanut Koleroga (Fruit Rot), Bud Rot, Ring Spot, and Yellow Leaf Phytoplasma Management'
    },
    'Madhya Pradesh': {
      datasetName: 'Annotated Mahua Leaf Disease Dataset & PlantVillage Benchmark',
      sourceOrg: 'Madhya Pradesh Council of Science and Technology (MPCST), VIT Bhopal University, JNKVV Jabalpur & RVSKVV Gwalior (DOI: 10.17632/6xjn6p73h7.1)',
      cropsCovered: 'Mahua, Soybean, Wheat, Tomato, Potato, Maize, and 14 Agricultural Crops',
      classesCount: '38 Core Plant Pathology Classes + Mahua Foliar Categories',
      imageRecords: '54,306 Benchmark Images + 5,327 Repository Files (451 Verified Annotations)',
      geoCoverage: 'Madhya Pradesh (All 55 Districts across Malwa, Nimar, Bundelkhand, Mahakoshal, and Chambal)',
      licenceAttribution: 'Creative Commons Attribution 4.0 International (CC BY 4.0) & CC0 1.0',
      regionalFocus: 'Central India Soybean Rust, Wheat Rusts, and Agro-Forestry Canopy Protection'
    },
    'Gujarat': {
      datasetName: 'PlantVillage Crop Disease Benchmark & Gujarat SAU Extension Protocols',
      sourceOrg: 'Penn State University / EPFL & Gujarat State Agricultural Universities (AAU Anand, JAU Junagadh, NAU Navsari, SDAU)',
      cropsCovered: 'Tomato, Potato, Pepper, Citrus, Maize, Squash, and 14 Agricultural Crops',
      classesCount: '38 Verified Plant Pathology Classes',
      imageRecords: '54,306 Verified Agricultural Leaf Photographs',
      geoCoverage: 'Gujarat (All 33 Districts across Saurashtra, North Gujarat, Middle Gujarat, and South Gujarat Heavy Rainfall Zone)',
      licenceAttribution: 'Creative Commons CC0 1.0 Universal (Public Domain Dedication)',
      regionalFocus: 'Vegetable Blights, Citrus Greening (HLB), Powdery Mildew, and University Extension Management'
    },
    'Haryana': {
      datasetName: 'PlantVillage Crop Disease Benchmark & CCS HAU Extension Protocols',
      sourceOrg: 'Penn State University / EPFL & Chaudhary Charan Singh Haryana Agricultural University (CCS HAU Hisar)',
      cropsCovered: 'Potato, Tomato, Pepper, Maize, Squash, and 14 Agricultural Crops',
      classesCount: '38 Verified Plant Pathology Classes',
      imageRecords: '54,306 Verified Agricultural Leaf Photographs',
      geoCoverage: 'Haryana (All 22 Districts across Eastern Plain, Western Semi-Arid, and Shivalik Foothills)',
      licenceAttribution: 'Creative Commons CC0 1.0 Universal (Public Domain Dedication)',
      regionalFocus: 'Potato Early/Late Blight, Solanaceous Bacterial Spot, and Yamuna Plain Mildew Protocols'
    }
  };

  private readonly defaultDatasetMetadata: DiseaseDatasetInfo = {
    datasetName: 'PlantVillage Open Crop Disease Repository & National ICAR Guidelines',
    sourceOrg: 'Penn State University, EPFL, & National ICAR Agricultural Extension Bulletins',
    cropsCovered: '14 Core Agricultural Crops (Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato)',
    classesCount: '38 Distinct Plant Pathology Classes',
    imageRecords: '54,306 Verified Leaf Photographs',
    geoCoverage: 'National Agricultural Reference with Verified State Extension Bulletins',
    licenceAttribution: 'Creative Commons CC0 1.0 Universal (Public Domain Dedication)',
    regionalFocus: 'Integrated Pest & Disease Management across standard agronomic crop varieties'
  };

  currentDatasetInfo: DiseaseDatasetInfo = this.stateDatasetMetadata['Maharashtra'];

  constructor(
    private diseaseService: DiseaseService,
    public locationService: LocationService
  ) {
    this.states = this.locationService.getStates();
    this.districts = this.locationService.getDistricts('Maharashtra');
    this.updateDatasetInfo();
  }

  onStateChange(): void {
    this.districts = this.locationService.getDistricts(this.selectedState);
    if (this.districts.length > 0) {
      this.selectedDistrict = this.districts[0];
    }
    this.updateDatasetInfo();
  }

  private updateDatasetInfo(): void {
    this.currentDatasetInfo = this.stateDatasetMetadata[this.selectedState] || this.defaultDatasetMetadata;
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
  }
}
