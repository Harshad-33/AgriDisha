import { Injectable } from '@angular/core';

export interface DistrictInfo {
  name: string;
  isVerified: boolean;
  region?: string;
  datasetLevel?: 'verified_primary' | 'regional_reference' | 'fallback';
}

@Injectable({
  providedIn: 'root'
})
export class LocationService {
  // Priority 1: Empirical verified trials dataset (Western Maharashtra)
  private primaryVerifiedDistricts = new Set<string>([
    'kolhapur',
    'satara',
    'sangli',
    'solapur',
    'pune'
  ]);

  // Priority 2: Expanded regional reference dataset (Remaining 31 Maharashtra districts)
  private expandedReferenceDistricts = new Set<string>([
    'ahmednagar',
    'akola',
    'amravati',
    'beed',
    'bhandara',
    'buldhana',
    'chandrapur',
    'chhatrapati sambhajinagar (aurangabad)',
    'aurangabad',
    'chhatrapati sambhajinagar',
    'dharashiv (osmanabad)',
    'osmanabad',
    'dharashiv',
    'dhule',
    'gadchiroli',
    'gondia',
    'hingoli',
    'jalgaon',
    'jalna',
    'latur',
    'mumbai city',
    'mumbai suburban',
    'nagpur',
    'nanded',
    'nandurbar',
    'nashik',
    'palghar',
    'parbhani',
    'raigad',
    'ratnagiri',
    'sindhudurg',
    'thane',
    'wardha',
    'washim',
    'yavatmal'
  ]);

  private maharashtraDistricts: string[] = [
    'Ahmednagar',
    'Akola',
    'Amravati',
    'Beed',
    'Bhandara',
    'Buldhana',
    'Chandrapur',
    'Chhatrapati Sambhajinagar (Aurangabad)',
    'Dharashiv (Osmanabad)',
    'Dhule',
    'Gadchiroli',
    'Gondia',
    'Hingoli',
    'Jalgaon',
    'Jalna',
    'Kolhapur',
    'Latur',
    'Mumbai City',
    'Mumbai Suburban',
    'Nagpur',
    'Nanded',
    'Nandurbar',
    'Nashik',
    'Palghar',
    'Parbhani',
    'Pune',
    'Raigad',
    'Ratnagiri',
    'Sangli',
    'Satara',
    'Sindhudurg',
    'Solapur',
    'Thane',
    'Wardha',
    'Washim',
    'Yavatmal'
  ];

  private indianStates: string[] = [
    'Maharashtra',
    'Andhra Pradesh',
    'Gujarat',
    'Haryana',
    'Karnataka',
    'Madhya Pradesh',
    'Punjab',
    'Rajasthan',
    'Tamil Nadu',
    'Telangana',
    'Uttar Pradesh',
    'West Bengal'
  ];

  private soilColors: string[] = [
    'Black Soil (Regur)',
    'Red Soil',
    'Medium Black Soil',
    'Alluvial Soil',
    'Laterite Soil',
    'Sandy Loam'
  ];

  getStates(): string[] {
    return this.indianStates;
  }

  getDistricts(state: string): string[] {
    if (state === 'Maharashtra') {
      return this.maharashtraDistricts;
    }
    return ['Central District', 'North District', 'South District', 'East District', 'West District'];
  }

  getDistrictDatasetStatus(state: string, district: string): 'verified_primary' | 'regional_reference' | 'fallback' {
    if (!state || !district) return 'fallback';
    if (state.toLowerCase().trim() !== 'maharashtra') return 'fallback';
    
    const clean = district.toLowerCase().trim();
    for (const vd of this.primaryVerifiedDistricts) {
      if (clean === vd || clean.includes(vd)) {
        return 'verified_primary';
      }
    }
    for (const ed of this.expandedReferenceDistricts) {
      if (clean === ed || clean.includes(ed)) {
        return 'regional_reference';
      }
    }
    return 'fallback';
  }

  isVerifiedDistrict(state: string, district: string): boolean {
    return this.getDistrictDatasetStatus(state, district) !== 'fallback';
  }

  isPrimaryVerified(state: string, district: string): boolean {
    return this.getDistrictDatasetStatus(state, district) === 'verified_primary';
  }

  isRegionalReference(state: string, district: string): boolean {
    return this.getDistrictDatasetStatus(state, district) === 'regional_reference';
  }

  getDistrictBadgeLabel(state: string, district: string): string {
    const status = this.getDistrictDatasetStatus(state, district);
    if (status === 'verified_primary') return '🟢 (Verified Dataset)';
    if (status === 'regional_reference') return '🔵 (Regional Reference)';
    return '';
  }

  getSoilColors(): string[] {
    return this.soilColors;
  }
}
