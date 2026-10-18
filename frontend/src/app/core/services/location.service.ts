import { Injectable } from '@angular/core';

export interface DistrictInfo {
  name: string;
  isVerified: boolean;
  region?: string;
}

@Injectable({
  providedIn: 'root'
})
export class LocationService {
  private verifiedDistricts = new Set<string>([
    'kolhapur',
    'satara',
    'sangli',
    'solapur',
    'pune'
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

  isVerifiedDistrict(state: string, district: string): boolean {
    if (!state || !district) return false;
    if (state.toLowerCase() !== 'maharashtra') return false;
    return this.verifiedDistricts.has(district.toLowerCase().trim());
  }

  getSoilColors(): string[] {
    return this.soilColors;
  }
}
