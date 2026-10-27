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

  // Priority 3: Telangana Regional Reference Dataset (All 33 Telangana districts)
  private telanganaReferenceDistricts = new Set<string>([
    'adilabad',
    'bhadradri kothagudem',
    'kothagudem',
    'hanumakonda',
    'warangal urban',
    'hyderabad',
    'jagtial',
    'jangaon',
    'jayashankar bhupalpally',
    'bhupalpally',
    'jogulamba gadwal',
    'gadwal',
    'kamareddy',
    'karimnagar',
    'khammam',
    'kumuram bheem asifabad',
    'asifabad',
    'mahabubabad',
    'mahabubnagar',
    'mancherial',
    'medak',
    'medchal-malkajgiri',
    'malkajgiri',
    'mulugu',
    'nagarkurnool',
    'nalgonda',
    'narayanpet',
    'nirmal',
    'nizamabad',
    'peddapalli',
    'rajanna sircilla',
    'sircilla',
    'ranga reddy',
    'sangareddy',
    'siddipet',
    'suryapet',
    'vikarabad',
    'wanaparthy',
    'warangal',
    'warangal rural',
    'yadadri bhuvanagiri',
    'bhuvanagiri',
    'bhongir'
  ]);

  private telanganaDistricts: string[] = [
    'Adilabad',
    'Bhadradri Kothagudem',
    'Hanumakonda',
    'Hyderabad',
    'Jagtial',
    'Jangaon',
    'Jayashankar Bhupalpally',
    'Jogulamba Gadwal',
    'Kamareddy',
    'Karimnagar',
    'Khammam',
    'Kumuram Bheem Asifabad',
    'Mahabubabad',
    'Mahabubnagar',
    'Mancherial',
    'Medak',
    'Medchal-Malkajgiri',
    'Mulugu',
    'Nagarkurnool',
    'Nalgonda',
    'Narayanpet',
    'Nirmal',
    'Nizamabad',
    'Peddapalli',
    'Rajanna Sircilla',
    'Ranga Reddy',
    'Sangareddy',
    'Siddipet',
    'Suryapet',
    'Vikarabad',
    'Wanaparthy',
    'Warangal',
    'Yadadri Bhuvanagiri'
  ];

  // Priority 4: Andhra Pradesh Regional Reference Dataset (All 26 Andhra Pradesh districts)
  private andhraReferenceDistricts = new Set<string>([
    'alluri sitharama raju',
    'alluri sitarama raju',
    'alluri',
    'anakapalli',
    'ananthapuramu',
    'anantapur',
    'annamayya',
    'bapatla',
    'chittoor',
    'dr. b.r. ambedkar konaseema',
    'dr b r ambedkar konaseema',
    'konaseema',
    'east godavari',
    'eluru',
    'guntur',
    'kakinada',
    'krishna',
    'kurnool',
    'nandyal',
    'ntr',
    'vijayawada',
    'palnadu',
    'parvathipuram manyam',
    'parvathipuram',
    'manyam',
    'prakasam',
    'spsr nellore',
    'nellore',
    'sri sathya sai',
    'sathya sai',
    'srikakulam',
    'tirupati',
    'visakhapatnam',
    'vizianagaram',
    'west godavari',
    'ysr kadapa',
    'kadapa',
    'cuddapah'
  ]);

  private andhraPradeshDistricts: string[] = [
    'Alluri Sitharama Raju',
    'Anakapalli',
    'Ananthapuramu',
    'Annamayya',
    'Bapatla',
    'Chittoor',
    'Dr. B.R. Ambedkar Konaseema',
    'East Godavari',
    'Eluru',
    'Guntur',
    'Kakinada',
    'Krishna',
    'Kurnool',
    'Nandyal',
    'NTR',
    'Palnadu',
    'Parvathipuram Manyam',
    'Prakasam',
    'SPSR Nellore',
    'Sri Sathya Sai',
    'Srikakulam',
    'Tirupati',
    'Visakhapatnam',
    'Vizianagaram',
    'West Godavari',
    'YSR Kadapa'
  ];

  // Priority 5: Gujarat Regional Reference Dataset (All 33 Gujarat districts)
  private gujaratReferenceDistricts = new Set<string>([
    'ahmadabad',
    'ahmedabad',
    'amreli',
    'anand',
    'aravalli',
    'banas kantha',
    'banaskantha',
    'bharuch',
    'bhavnagar',
    'botad',
    'chhota udepur',
    'chhotaudepur',
    'chhota udaipur',
    'dang',
    'dangs',
    'the dangs',
    'devbhumi dwarka',
    'devbhoomi dwarka',
    'dwarka',
    'dohad',
    'dahod',
    'gandhinagar',
    'gir somnath',
    'somnath',
    'jamnagar',
    'junagadh',
    'kachchh',
    'kutch',
    'kheda',
    'mahesana',
    'mehsana',
    'mahisagar',
    'morbi',
    'narmada',
    'navsari',
    'panch mahals',
    'panchmahal',
    'panchmahals',
    'patan',
    'porbandar',
    'rajkot',
    'sabar kantha',
    'sabarkantha',
    'surat',
    'surendranagar',
    'tapi',
    'vadodara',
    'valsad'
  ]);

  private gujaratDistricts: string[] = [
    'Ahmadabad (Ahmedabad)',
    'Amreli',
    'Anand',
    'Aravalli',
    'Banas Kantha (Banaskantha)',
    'Bharuch',
    'Bhavnagar',
    'Botad',
    'Chhota Udepur',
    'Dang (The Dangs)',
    'Devbhumi Dwarka',
    'Dohad (Dahod)',
    'Gandhinagar',
    'Gir Somnath',
    'Jamnagar',
    'Junagadh',
    'Kachchh (Kutch)',
    'Kheda',
    'Mahesana (Mehsana)',
    'Mahisagar',
    'Morbi',
    'Narmada',
    'Navsari',
    'Panch Mahals (Panchmahal)',
    'Patan',
    'Porbandar',
    'Rajkot',
    'Sabar Kantha (Sabarkantha)',
    'Surat',
    'Surendranagar',
    'Tapi',
    'Vadodara',
    'Valsad'
  ];

  // Priority 6: Haryana Regional Reference Dataset (All 22 Haryana districts)
  private haryanaReferenceDistricts = new Set<string>([
    'ambala',
    'bhiwani',
    'charkhi dadri',
    'charki dadri',
    'charkidadri',
    'faridabad',
    'fatehabad',
    'gurugram',
    'gurgaon',
    'hisar',
    'hissar',
    'jhajjar',
    'jind',
    'kaithal',
    'karnal',
    'kurukshetra',
    'mahendragarh',
    'narnaul',
    'mohindergarh',
    'nuh',
    'mewat',
    'palwal',
    'panchkula',
    'panipat',
    'rewari',
    'rohtak',
    'sirsa',
    'sonipat',
    'sonepat',
    'yamunanagar'
  ]);

  private haryanaDistricts: string[] = [
    'Ambala',
    'Bhiwani',
    'Charkhi Dadri',
    'Faridabad',
    'Fatehabad',
    'Gurugram (Gurgaon)',
    'Hisar (Hissar)',
    'Jhajjar',
    'Jind',
    'Kaithal',
    'Karnal',
    'Kurukshetra',
    'Mahendragarh (Narnaul)',
    'Nuh (Mewat)',
    'Palwal',
    'Panchkula',
    'Panipat',
    'Rewari',
    'Rohtak',
    'Sirsa',
    'Sonipat (Sonepat)',
    'Yamunanagar'
  ];

  // Priority 7: Karnataka Regional Reference Dataset (All 31 Karnataka districts)
  private karnatakaReferenceDistricts = new Set<string>([
    'bagalkote',
    'bagalkot',
    'ballari',
    'bellary',
    'belagavi',
    'belgaum',
    'bengaluru rural',
    'bangalore rural',
    'bengaluru urban',
    'bangalore urban',
    'bangalore',
    'bengaluru',
    'bidar',
    'chamarajanagara',
    'chamarajanagar',
    'chikkaballapura',
    'chikballapur',
    'chikkaballapur',
    'chikkamagaluru',
    'chikmagalur',
    'chikmagalore',
    'chikkamagalur',
    'chitradurga',
    'dakshina kannada',
    'dakshin kannad',
    'south canara',
    'davanagere',
    'davangere',
    'dharwad',
    'gadag',
    'hassan',
    'haveri',
    'kalaburagi',
    'gulbarga',
    'kodagu',
    'coorg',
    'kolar',
    'koppal',
    'mandya',
    'mysuru',
    'mysore',
    'raichur',
    'ramanagara',
    'ramanagar',
    'shivamogga',
    'shimoga',
    'tumakuru',
    'tumkur',
    'udupi',
    'uttara kannada',
    'uttar kannad',
    'north canara',
    'vijayanagara',
    'hospet',
    'vijayapura',
    'bijapur',
    'yadgir'
  ]);

  private karnatakaDistricts: string[] = [
    'Bagalkote',
    'Ballari (Bellary)',
    'Belagavi (Belgaum)',
    'Bengaluru Rural',
    'Bengaluru Urban',
    'Bidar',
    'Chamarajanagara',
    'Chikkaballapura',
    'Chikkamagaluru (Chikmagalur)',
    'Chitradurga',
    'Dakshina Kannada (Mangaluru)',
    'Davanagere',
    'Dharwad',
    'Gadag',
    'Hassan',
    'Haveri',
    'Kalaburagi (Gulbarga)',
    'Kodagu (Coorg)',
    'Kolar',
    'Koppal',
    'Mandya',
    'Mysuru (Mysore)',
    'Raichur',
    'Ramanagara',
    'Shivamogga (Shimoga)',
    'Tumakuru (Tumkur)',
    'Udupi',
    'Uttara Kannada (Karwar)',
    'Vijayanagara (Hospet)',
    'Vijayapura (Bijapur)',
    'Yadgir'
  ];




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
    if (state === 'Telangana') {
      return this.telanganaDistricts;
    }
    if (state === 'Andhra Pradesh') {
      return this.andhraPradeshDistricts;
    }
    if (state === 'Gujarat') {
      return this.gujaratDistricts;
    }
    if (state === 'Haryana') {
      return this.haryanaDistricts;
    }
    if (state === 'Karnataka') {
      return this.karnatakaDistricts;
    }
    return ['Central District', 'North District', 'South District', 'East District', 'West District'];
  }

  getDistrictDatasetStatus(state: string, district: string): 'verified_primary' | 'regional_reference' | 'fallback' {
    if (!state || !district) return 'fallback';
    const clean = district.toLowerCase().trim();
    const st = state.toLowerCase().trim();

    if (st === 'maharashtra') {
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
    }

    if (st === 'telangana') {
      for (const td of this.telanganaReferenceDistricts) {
        if (clean === td || clean.includes(td) || td.includes(clean)) {
          return 'regional_reference';
        }
      }
    }

    if (st === 'andhra pradesh') {
      for (const ad of this.andhraReferenceDistricts) {
        if (clean === ad || clean.includes(ad) || ad.includes(clean)) {
          return 'regional_reference';
        }
      }
    }

    if (st === 'gujarat') {
      for (const gd of this.gujaratReferenceDistricts) {
        if (clean === gd || clean.includes(gd) || gd.includes(clean)) {
          return 'regional_reference';
        }
      }
    }

    if (st === 'haryana') {
      for (const hd of this.haryanaReferenceDistricts) {
        if (clean === hd || clean.includes(hd) || hd.includes(clean)) {
          return 'regional_reference';
        }
      }
    }

    if (st === 'karnataka') {
      for (const kd of this.karnatakaReferenceDistricts) {
        if (clean === kd || clean.includes(kd) || kd.includes(clean)) {
          return 'regional_reference';
        }
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
