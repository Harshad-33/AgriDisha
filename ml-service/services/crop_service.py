"""
Maharashtra District-Aware Crop Recommendation Service.
Combines Random Forest model trained on Maharashtra agronomic dataset (maharashtra_crop_data.csv)
with district-level agro-climatic intelligence from ICAR, MPKV Rahuri, PDKV Akola, VNMKV Parbhani, and BSKKV Dapoli.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
import numpy as np
import joblib
from services.dataset_manager import DatasetManager

logger = logging.getLogger("ml_service.crop")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_recommendation.joblib")
DISTRICTS_PATH = os.path.join(BASE_DIR, "data", "maharashtra_districts.json")

CROP_DISPLAY_NAMES = {
    'cotton': 'Cotton (Bt Cotton / Kapas)',
    'soybean': 'Soybean (Soya)',
    'pigeonpeas': 'Pigeon Pea (Tur / Arhar)',
    'sorghum': 'Sorghum (Jowar / Maldandi)',
    'chickpea': 'Chickpea (Gram / Harbara)',
    'sugarcane': 'Sugarcane (Oos)',
    'onion': 'Onion (Kanda)',
    'grapes': 'Grapes (Draksha)',
    'pomegranate': 'Pomegranate (Dalimb - Bhagwa)',
    'banana': 'Banana (Keli - Grand Naine)',
    'orange': 'Orange (Nagpur Mandarin / Santra)',
    'sweet_lime': 'Sweet Lime (Mosambi)',
    'mango': 'Mango (Alphonso / Hapus)',
    'cashew': 'Cashew (Kaju)',
    'rice': 'Rice (Paddy / Bhat)',
    'wheat': 'Wheat (Gahu - Sharbati / Lokwan)',
    'maize': 'Maize (Makka)',
    'bajra': 'Pearl Millet (Bajra)',
    'ragi': 'Finger Millet (Nachani / Ragi)',
    'groundnut': 'Groundnut (Bhuimug)',
    'tomato': 'Tomato',
    'coconut': 'Coconut (Naral)'
}

# District alias mapping for Maharashtra
DISTRICT_ZONE_MAP = {
    # Central Vidarbha (Cotton, Soybean, Tur, Jowar, Orange, Harbara)
    'yavatmal': 'Central Vidarbha Zone',
    'wardha': 'Central Vidarbha Zone',
    'nagpur': 'Central Vidarbha Zone',
    'amravati': 'Central Vidarbha Zone',
    'akola': 'Central Vidarbha Zone',
    'buldhana': 'Central Vidarbha Zone',
    'washim': 'Central Vidarbha Zone',

    # Eastern Vidarbha (Rice / Paddy, Soybean, Cotton)
    'chandrapur': 'Eastern Vidarbha (Wainganga Basin)',
    'bhandara': 'Eastern Vidarbha (Wainganga Basin)',
    'gondia': 'Eastern Vidarbha (Wainganga Basin)',
    'gadchiroli': 'Eastern Vidarbha (Wainganga Basin)',

    # Marathwada (Soybean, Cotton, Tur, Jowar, Mosambi)
    'latur': 'Central Maharashtra (Marathwada)',
    'nanded': 'Central Maharashtra (Marathwada)',
    'parbhani': 'Central Maharashtra (Marathwada)',
    'hingoli': 'Central Maharashtra (Marathwada)',
    'beed': 'Central Maharashtra (Marathwada)',
    'jalna': 'Central Maharashtra (Marathwada)',
    'aurangabad': 'Central Maharashtra (Marathwada)',
    'chhatrapati sambhajinagar': 'Central Maharashtra (Marathwada)',
    'sambhajinagar': 'Central Maharashtra (Marathwada)',
    'osmanabad': 'Central Maharashtra (Marathwada)',
    'dharashiv': 'Central Maharashtra (Marathwada)',

    # Western Maharashtra (Sugarcane, Grapes, Onion, Tomato, Pomegranate)
    'nashik': 'Western Maharashtra Plain',
    'pune': 'Western Maharashtra Plain',
    'satara': 'Western Maharashtra Plain',
    'kolhapur': 'Western Maharashtra Plain',
    'sangli': 'Western Maharashtra Plain',
    'solapur': 'Scarcity & Rain Shadow Zone',
    'ahmednagar': 'Scarcity & Rain Shadow Zone',
    'ahilyanagar': 'Scarcity & Rain Shadow Zone',

    # Khandesh (Banana, Cotton, Maize, Jowar)
    'jalgaon': 'Khandesh & Tapi Basin',
    'dhule': 'Khandesh & Tapi Basin',
    'nandurbar': 'Khandesh & Tapi Basin',

    # Konkan (Alphonso Mango, Cashew, Rice, Coconut)
    'ratnagiri': 'South Konkan',
    'sindhudurg': 'South Konkan',
    'raigad': 'North Konkan',
    'thane': 'North Konkan',
    'palghar': 'North Konkan',
    'mumbai': 'North Konkan',
    'mumbai city': 'North Konkan',
    'mumbai suburban': 'North Konkan'
}

# District alias mapping for Telangana Agro-Climatic Zones (PJTSAU)
TELANGANA_DISTRICT_ZONE_MAP = {
    # Northern Telangana Zone (PJTSAU RARS Jagtial: Cotton, Soybean, Paddy, Maize, Turmeric)
    'adilabad': 'Northern Telangana Zone',
    'nirmal': 'Northern Telangana Zone',
    'kumuram bheem asifabad': 'Northern Telangana Zone',
    'asifabad': 'Northern Telangana Zone',
    'mancherial': 'Northern Telangana Zone',
    'nizamabad': 'Northern Telangana Zone',
    'kamareddy': 'Northern Telangana Zone',
    'jagtial': 'Northern Telangana Zone',
    'peddapalli': 'Northern Telangana Zone',
    'karimnagar': 'Northern Telangana Zone',
    'rajanna sircilla': 'Northern Telangana Zone',
    'sircilla': 'Northern Telangana Zone',

    # Central Telangana Zone (PJTSAU RARS Warangal: Cotton, Chilli, Paddy, Maize, Pulses)
    'warangal': 'Central Telangana Zone',
    'hanumakonda': 'Central Telangana Zone',
    'warangal urban': 'Central Telangana Zone',
    'warangal rural': 'Central Telangana Zone',
    'jangaon': 'Central Telangana Zone',
    'jayashankar bhupalpally': 'Central Telangana Zone',
    'bhupalpally': 'Central Telangana Zone',
    'mahabubabad': 'Central Telangana Zone',
    'mulugu': 'Central Telangana Zone',
    'khammam': 'Central Telangana Zone',
    'bhadradri kothagudem': 'Central Telangana Zone',
    'kothagudem': 'Central Telangana Zone',

    # Southern Telangana Zone (PJTSAU Palem / Rajendranagar: Paddy, Cotton, Castor, Redgram, Groundnut)
    'nalgonda': 'Southern Telangana Zone',
    'suryapet': 'Southern Telangana Zone',
    'yadadri bhuvanagiri': 'Southern Telangana Zone',
    'bhongir': 'Southern Telangana Zone',
    'mahabubnagar': 'Southern Telangana Zone',
    'nagarkurnool': 'Southern Telangana Zone',
    'wanaparthy': 'Southern Telangana Zone',
    'jogulamba gadwal': 'Southern Telangana Zone',
    'gadwal': 'Southern Telangana Zone',
    'narayanpet': 'Southern Telangana Zone',
    'medak': 'Southern Telangana Zone',
    'sangareddy': 'Southern Telangana Zone',
    'siddipet': 'Southern Telangana Zone',
    'vikarabad': 'Southern Telangana Zone',
    'ranga reddy': 'Southern Telangana Zone',
    'medchal-malkajgiri': 'Southern Telangana Zone',
    'malkajgiri': 'Southern Telangana Zone',
    'hyderabad': 'Southern Telangana Zone'
}

# District alias mapping for Andhra Pradesh Agro-Climatic Zones (ANGRAU / Dr. YSRHU)
ANDHRA_PRADESH_DISTRICT_ZONE_MAP = {
    # North Coastal Zone (Paddy, Sugarcane, Cashew, Mango, Groundnut)
    'srikakulam': 'North Coastal Andhra Zone',
    'vizianagaram': 'North Coastal Andhra Zone',
    'parvathipuram manyam': 'North Coastal Andhra Zone',
    'parvathipuram': 'North Coastal Andhra Zone',
    'manyam': 'North Coastal Andhra Zone',
    'visakhapatnam': 'North Coastal Andhra Zone',
    'anakapalli': 'North Coastal Andhra Zone',
    'alluri sitharama raju': 'North Coastal Andhra Zone',
    'alluri': 'North Coastal Andhra Zone',

    # Godavari Delta Zone (Paddy, Coconut, Banana, Sugarcane, Oil Palm)
    'east godavari': 'Godavari Delta Zone',
    'kakinada': 'Godavari Delta Zone',
    'dr. b.r. ambedkar konaseema': 'Godavari Delta Zone',
    'konaseema': 'Godavari Delta Zone',
    'west godavari': 'Godavari Delta Zone',
    'eluru': 'Godavari Delta Zone',

    # Krishna Delta & Chili Belt Zone (Cotton, Chili, Paddy, Maize, Pulses)
    'krishna': 'Krishna Delta & Chili Belt Zone',
    'ntr': 'Krishna Delta & Chili Belt Zone',
    'vijayawada': 'Krishna Delta & Chili Belt Zone',
    'guntur': 'Krishna Delta & Chili Belt Zone',
    'bapatla': 'Krishna Delta & Chili Belt Zone',
    'palnadu': 'Krishna Delta & Chili Belt Zone',
    'prakasam': 'Krishna Delta & Chili Belt Zone',

    # Southern Zone (Groundnut, Tomato, Rice, Mango, Sugarcane)
    'spsr nellore': 'Southern Andhra Zone',
    'nellore': 'Southern Andhra Zone',
    'tirupati': 'Southern Andhra Zone',
    'chittoor': 'Southern Andhra Zone',
    'annamayya': 'Southern Andhra Zone',
    'ysr kadapa': 'Southern Andhra Zone',
    'kadapa': 'Southern Andhra Zone',

    # Scarce Rainfall Zone of Rayalaseema (Groundnut, Bengalgram/Chickpea, Cotton, Sorghum)
    'kurnool': 'Scarce Rainfall Zone of Rayalaseema',
    'nandyal': 'Scarce Rainfall Zone of Rayalaseema',
    'ananthapuramu': 'Scarce Rainfall Zone of Rayalaseema',
    'anantapur': 'Scarce Rainfall Zone of Rayalaseema',
    'sri sathya sai': 'Scarce Rainfall Zone of Rayalaseema',
    'sathya sai': 'Scarce Rainfall Zone of Rayalaseema'
}

# District alias mapping for Gujarat Agro-Climatic Zones (AAU / JAU / NAU / SDAU)
GUJARAT_DISTRICT_ZONE_MAP = {
    # Middle Gujarat Zone (Anand Agricultural University - AAU, Anand)
    'anand': 'Middle Gujarat Zone (AAU Anand)',
    'kheda': 'Middle Gujarat Zone (AAU Anand)',
    'vadodara': 'Middle Gujarat Zone (AAU Anand)',
    'panch mahals': 'Middle Gujarat Zone (AAU Anand)',
    'panchmahal': 'Middle Gujarat Zone (AAU Anand)',
    'panchmahals': 'Middle Gujarat Zone (AAU Anand)',
    'dohad': 'Middle Gujarat Zone (AAU Anand)',
    'dahod': 'Middle Gujarat Zone (AAU Anand)',
    'mahisagar': 'Middle Gujarat Zone (AAU Anand)',
    'chhota udepur': 'Middle Gujarat Zone (AAU Anand)',
    'chhotaudepur': 'Middle Gujarat Zone (AAU Anand)',

    # Saurashtra & Coastal Zone (Junagadh Agricultural University - JAU, Junagadh)
    'junagadh': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'rajkot': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'jamnagar': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'porbandar': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'amreli': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'bhavnagar': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'surendranagar': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'gir somnath': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'somnath': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'botad': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'devbhumi dwarka': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'dwarka': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'morbi': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'ahmadabad': 'Saurashtra & Coastal Zone (JAU Junagadh)',
    'ahmedabad': 'Saurashtra & Coastal Zone (JAU Junagadh)',

    # North Gujarat & Arid Zone (SDAU, Sardarkrushinagar)
    'banas kantha': 'North Gujarat & Arid Zone (SDAU)',
    'banaskantha': 'North Gujarat & Arid Zone (SDAU)',
    'sabar kantha': 'North Gujarat & Arid Zone (SDAU)',
    'sabarkantha': 'North Gujarat & Arid Zone (SDAU)',
    'patan': 'North Gujarat & Arid Zone (SDAU)',
    'mahesana': 'North Gujarat & Arid Zone (SDAU)',
    'mehsana': 'North Gujarat & Arid Zone (SDAU)',
    'gandhinagar': 'North Gujarat & Arid Zone (SDAU)',
    'aravalli': 'North Gujarat & Arid Zone (SDAU)',
    'kachchh': 'North Gujarat & Arid Zone (SDAU)',
    'kutch': 'North Gujarat & Arid Zone (SDAU)',

    # South Gujarat Heavy Rainfall Zone (Navsari Agricultural University - NAU, Navsari)
    'navsari': 'South Gujarat Heavy Rainfall Zone (NAU Navsari)',
    'surat': 'South Gujarat Heavy Rainfall Zone (NAU Navsari)',
    'bharuch': 'South Gujarat Heavy Rainfall Zone (NAU Navsari)',
    'valsad': 'South Gujarat Heavy Rainfall Zone (NAU Navsari)',
    'dang': 'South Gujarat Heavy Rainfall Zone (NAU Navsari)',
    'the dangs': 'South Gujarat Heavy Rainfall Zone (NAU Navsari)',
    'dangs': 'South Gujarat Heavy Rainfall Zone (NAU Navsari)',
    'narmada': 'South Gujarat Heavy Rainfall Zone (NAU Navsari)',
    'tapi': 'South Gujarat Heavy Rainfall Zone (NAU Navsari)'
}

# District alias mapping for Haryana Agro-Climatic Zones (CCS HAU Hisar)
HARYANA_DISTRICT_ZONE_MAP = {
    # Eastern Agrozone (Yamuna Basin - CCS HAU Karnal / Kaul)
    'ambala': 'Eastern Agrozone (Yamuna Basin - CCS HAU)',
    'panchkula': 'Eastern Agrozone (Yamuna Basin - CCS HAU)',
    'yamunanagar': 'Eastern Agrozone (Yamuna Basin - CCS HAU)',
    'kurukshetra': 'Eastern Agrozone (Yamuna Basin - CCS HAU)',
    'karnal': 'Eastern Agrozone (Yamuna Basin - CCS HAU)',
    'kaithal': 'Eastern Agrozone (Yamuna Basin - CCS HAU)',
    'panipat': 'Eastern Agrozone (Yamuna Basin - CCS HAU)',
    'sonipat': 'Eastern Agrozone (Yamuna Basin - CCS HAU)',
    'sonepat': 'Eastern Agrozone (Yamuna Basin - CCS HAU)',

    # Western Semi-Arid Zone (CCS HAU Hisar / Sirsa)
    'hisar': 'Western Semi-Arid Zone (CCS HAU Hisar)',
    'hissar': 'Western Semi-Arid Zone (CCS HAU Hisar)',
    'sirsa': 'Western Semi-Arid Zone (CCS HAU Hisar)',
    'fatehabad': 'Western Semi-Arid Zone (CCS HAU Hisar)',
    'bhiwani': 'Western Semi-Arid Zone (CCS HAU Hisar)',
    'charkhi dadri': 'Western Semi-Arid Zone (CCS HAU Hisar)',
    'charki dadri': 'Western Semi-Arid Zone (CCS HAU Hisar)',
    'rohtak': 'Western Semi-Arid Zone (CCS HAU Hisar)',
    'jhajjar': 'Western Semi-Arid Zone (CCS HAU Hisar)',
    'jind': 'Western Semi-Arid Zone (CCS HAU Hisar)',

    # Southern Arid & NCR Zone (CCS HAU RRS Bawal)
    'gurugram': 'Southern Arid & NCR Zone (CCS HAU Bawal)',
    'gurgaon': 'Southern Arid & NCR Zone (CCS HAU Bawal)',
    'faridabad': 'Southern Arid & NCR Zone (CCS HAU Bawal)',
    'rewari': 'Southern Arid & NCR Zone (CCS HAU Bawal)',
    'mahendragarh': 'Southern Arid & NCR Zone (CCS HAU Bawal)',
    'narnaul': 'Southern Arid & NCR Zone (CCS HAU Bawal)',
    'mohindergarh': 'Southern Arid & NCR Zone (CCS HAU Bawal)',
    'palwal': 'Southern Arid & NCR Zone (CCS HAU Bawal)',
    'nuh': 'Southern Arid & NCR Zone (CCS HAU Bawal)',
    'mewat': 'Southern Arid & NCR Zone (CCS HAU Bawal)'
}


# District alias mapping for Karnataka Agro-Climatic Zones (UAS Bangalore, UAS Dharwad & KSNUAHS Shivamogga)
KARNATAKA_DISTRICT_ZONE_MAP = {
    # Coastal & Malnad Zone (KSNUAHS Shivamogga: Arecanut, Rice, Coconut, Black Pepper, Coffee)
    'dakshina kannada': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'dakshin kannad': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'south canara': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'udupi': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'uttara kannada': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'uttar kannad': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'north canara': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'chikkamagaluru': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'chikmagalur': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'kodagu': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'coorg': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'shivamogga': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'shimoga': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',
    'hassan': 'Coastal & Malnad Zone (KSNUAHS Shivamogga)',

    # Southern Dry & Transition Zone (UAS Bangalore: Ragi, Maize, Sugarcane, Rice, Tomato)
    'bengaluru urban': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'bangalore urban': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'bangalore': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'bengaluru': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'bengaluru rural': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'bangalore rural': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'ramanagara': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'ramanagar': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'mandya': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'mysuru': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'mysore': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'chamarajanagara': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'chamarajanagar': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'tumakuru': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'tumkur': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'kolar': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'chikkaballapura': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'chikballapur': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'chitradurga': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'davanagere': 'Southern Dry & Transition Zone (UAS Bangalore)',
    'davangere': 'Southern Dry & Transition Zone (UAS Bangalore)',

    # Northern Dry & Transition Zone (UAS Dharwad & UAS Raichur: Jowar, Cotton, Tur, Chickpea, Groundnut)
    'belagavi': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'belgaum': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'dharwad': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'gadag': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'haveri': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'bagalkote': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'bagalkot': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'vijayapura': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'bijapur': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'ballari': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'bellary': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'vijayanagara': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'koppal': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'raichur': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'kalaburagi': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'gulbarga': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'yadgir': 'Northern Dry & Transition Zone (UAS Dharwad)',
    'bidar': 'Northern Dry & Transition Zone (UAS Dharwad)'
}

# District alias mapping for Madhya Pradesh Agro-Climatic Zones (JNKVV Jabalpur & RVSKVV Gwalior)
MADHYA_PRADESH_DISTRICT_ZONE_MAP = {
    # Malwa Plateau Zone (RVSKVV Gwalior / Indore: Soybean, Wheat, Gram, Garlic, Onion)
    'agar malwa': 'Malwa Plateau Zone (RVSKVV)',
    'agar-malwa': 'Malwa Plateau Zone (RVSKVV)',
    'dewas': 'Malwa Plateau Zone (RVSKVV)',
    'dhar': 'Malwa Plateau Zone (RVSKVV)',
    'indore': 'Malwa Plateau Zone (RVSKVV)',
    'mandsaur': 'Malwa Plateau Zone (RVSKVV)',
    'neemuch': 'Malwa Plateau Zone (RVSKVV)',
    'rajgarh': 'Malwa Plateau Zone (RVSKVV)',
    'ratlam': 'Malwa Plateau Zone (RVSKVV)',
    'shajapur': 'Malwa Plateau Zone (RVSKVV)',
    'ujjain': 'Malwa Plateau Zone (RVSKVV)',

    # Nimar Valley Zone (RVSKVV / Khargone: Cotton, Chilli, Banana, Soybean, Jowar)
    'barwani': 'Nimar Valley Zone (RVSKVV)',
    'burhanpur': 'Nimar Valley Zone (RVSKVV)',
    'khandwa': 'Nimar Valley Zone (RVSKVV)',
    'east nimar': 'Nimar Valley Zone (RVSKVV)',
    'khargone': 'Nimar Valley Zone (RVSKVV)',
    'west nimar': 'Nimar Valley Zone (RVSKVV)',

    # Gird Northern Zone (RVSKVV Gwalior: Mustard, Wheat, Bajra, Gram)
    'ashoknagar': 'Gird Northern Zone (RVSKVV Gwalior)',
    'bhind': 'Gird Northern Zone (RVSKVV Gwalior)',
    'guna': 'Gird Northern Zone (RVSKVV Gwalior)',
    'gwalior': 'Gird Northern Zone (RVSKVV Gwalior)',
    'morena': 'Gird Northern Zone (RVSKVV Gwalior)',
    'sheopur': 'Gird Northern Zone (RVSKVV Gwalior)',
    'shivpuri': 'Gird Northern Zone (RVSKVV Gwalior)',

    # Bundelkhand Zone (JNKVV Tikamgarh: Wheat, Gram, Mustard, Sesame)
    'chhatarpur': 'Bundelkhand Zone (JNKVV)',
    'datia': 'Bundelkhand Zone (JNKVV)',
    'niwari': 'Bundelkhand Zone (JNKVV)',
    'tikamgarh': 'Bundelkhand Zone (JNKVV)',

    # Central Narmada Valley (JNKVV Powarkheda: Wheat, Soybean, Sugarcane, Gram)
    'harda': 'Central Narmada Valley Zone (JNKVV)',
    'narmadapuram': 'Central Narmada Valley Zone (JNKVV)',
    'hoshangabad': 'Central Narmada Valley Zone (JNKVV)',
    'narsinghpur': 'Central Narmada Valley Zone (JNKVV)',

    # Vindhyan Plateau Zone (JNKVV Sehore: Wheat, Gram, Soybean, Lentil)
    'bhopal': 'Vindhyan Plateau Zone (JNKVV)',
    'damoh': 'Vindhyan Plateau Zone (JNKVV)',
    'raisen': 'Vindhyan Plateau Zone (JNKVV)',
    'sagar': 'Vindhyan Plateau Zone (JNKVV)',
    'sehore': 'Vindhyan Plateau Zone (JNKVV)',
    'vidisha': 'Vindhyan Plateau Zone (JNKVV)',

    # Kymore Plateau & Satpura Hills (JNKVV Jabalpur: Rice, Wheat, Gram, Tur)
    'jabalpur': 'Kymore Plateau & Satpura Hills (JNKVV Jabalpur)',
    'katni': 'Kymore Plateau & Satpura Hills (JNKVV Jabalpur)',
    'maihar': 'Kymore Plateau & Satpura Hills (JNKVV Jabalpur)',
    'mauganj': 'Kymore Plateau & Satpura Hills (JNKVV Jabalpur)',
    'panna': 'Kymore Plateau & Satpura Hills (JNKVV Jabalpur)',
    'rewa': 'Kymore Plateau & Satpura Hills (JNKVV Jabalpur)',
    'satna': 'Kymore Plateau & Satpura Hills (JNKVV Jabalpur)',
    'sidhi': 'Kymore Plateau & Satpura Hills (JNKVV Jabalpur)',
    'singrauli': 'Kymore Plateau & Satpura Hills (JNKVV Jabalpur)',

    # Satpura Plateau Zone (JNKVV Chhindwara: Maize, Soybean, Cotton, Orange)
    'betul': 'Satpura Plateau Zone (JNKVV)',
    'chhindwara': 'Satpura Plateau Zone (JNKVV)',
    'pandhurna': 'Satpura Plateau Zone (JNKVV)',

    # Jhabua Hills Zone (RVSKVV Jhabua: Maize, Cotton, Soybean, Millets)
    'alirajpur': 'Jhabua Hills Zone (RVSKVV)',
    'jhabua': 'Jhabua Hills Zone (RVSKVV)',

    # Eastern Plateau & Tribal Zone (JNKVV Shahdol / Balaghat: Rice, Millets, Niger)
    'anuppur': 'Eastern Plateau & Tribal Zone (JNKVV)',
    'dindori': 'Eastern Plateau & Tribal Zone (JNKVV)',
    'mandla': 'Eastern Plateau & Tribal Zone (JNKVV)',
    'seoni': 'Eastern Plateau & Tribal Zone (JNKVV)',
    'shahdol': 'Eastern Plateau & Tribal Zone (JNKVV)',
    'umaria': 'Eastern Plateau & Tribal Zone (JNKVV)',
    'balaghat': 'Wainganga Valley Zone (JNKVV Balaghat)'
}

# District alias mapping for Punjab Agro-Climatic Zones (PAU Ludhiana)
PUNJAB_DISTRICT_ZONE_MAP = {
    # Central Plain Zone (Rice-Wheat Intensive: PAU Ludhiana Main Campus)
    'amritsar': 'Central Plain Zone (Rice-Wheat)',
    'barnala': 'Central Plain Zone (Rice-Wheat)',
    'fatehgarh sahib': 'Central Plain Zone (Rice-Wheat)',
    'jalandhar': 'Central Plain Zone (Rice-Wheat)',
    'kapurthala': 'Central Plain Zone (Rice-Wheat)',
    'ludhiana': 'Central Plain Zone (Rice-Wheat)',
    'malerkotla': 'Central Plain Zone (Rice-Wheat)',
    'patiala': 'Central Plain Zone (Rice-Wheat)',
    'sangrur': 'Central Plain Zone (Rice-Wheat)',
    'tarn taran': 'Central Plain Zone (Rice-Wheat)',

    # South-Western Semi-Arid Zone (Cotton-Wheat Belt: PAU RRS Bathinda / Faridkot)
    'bathinda': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'bhatinda': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'faridkot': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'fazilka': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'firozpur': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'firozepur': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'ferozepur': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'mansa': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'moga': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'muktsar': 'South-Western Semi-Arid Zone (Cotton-Wheat)',
    'sri muktsar sahib': 'South-Western Semi-Arid Zone (Cotton-Wheat)',

    # Sub-Mountain Undulating Zone (Kandi Zone: PAU RRS Ballowal Saunkhri / Gurdaspur)
    'gurdaspur': 'Sub-Mountain Undulating Zone (Kandi)',
    'hoshiarpur': 'Sub-Mountain Undulating Zone (Kandi)',
    'pathankot': 'Sub-Mountain Undulating Zone (Kandi)',
    'rupnagar': 'Sub-Mountain Undulating Zone (Kandi)',
    'ropar': 'Sub-Mountain Undulating Zone (Kandi)',
    'sahibzada ajit singh nagar': 'Sub-Mountain Undulating Zone (Kandi)',
    'sas nagar': 'Sub-Mountain Undulating Zone (Kandi)',
    's.a.s. nagar': 'Sub-Mountain Undulating Zone (Kandi)',
    'mohali': 'Sub-Mountain Undulating Zone (Kandi)',
    'shahid bhagat singh nagar': 'Sub-Mountain Undulating Zone (Kandi)',
    'sbs nagar': 'Sub-Mountain Undulating Zone (Kandi)',
    's.b.s. nagar': 'Sub-Mountain Undulating Zone (Kandi)',
    'nawanshahr': 'Sub-Mountain Undulating Zone (Kandi)',
    'nawashahr': 'Sub-Mountain Undulating Zone (Kandi)'
}

class CropService:
    def _resolve_state(self, state, dataset_state, zone_name):
        if state and str(state).strip():
            return str(state).strip()
        if dataset_state and str(dataset_state).strip():
            return str(dataset_state).strip()
        z = zone_name or ""
        if any(kw in z for kw in ["Punjab", "Central Plain", "South-Western Semi-Arid", "Kandi", "PAU"]):
            return "Punjab"
        if any(kw in z for kw in ["Madhya Pradesh", "Malwa", "Nimar", "Gird", "Narmada Valley", "Bundelkhand", "Vindhyan", "Kymore", "Satpura", "RVSKVV", "JNKVV"]):
            return "Madhya Pradesh"
        if any(kw in z for kw in ["Karnataka", "Malnad", "KSNUAHS", "UAS Bangalore", "UAS Dharwad"]):
            return "Karnataka"
        if any(kw in z for kw in ["Haryana", "Yamuna Basin", "CCS HAU", "Hisar", "Bawal"]):
            return "Haryana"
        if any(kw in z for kw in ["Gujarat", "Saurashtra", "AAU", "JAU", "NAU", "SDAU"]):
            return "Gujarat"
        if any(kw in z for kw in ["Andhra", "Rayalaseema", "Godavari", "Krishna"]):
            return "Andhra Pradesh"
        if "Telangana" in z:
            return "Telangana"
        return "Maharashtra"

    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.model_payload: Optional[Dict[str, Any]] = None
        self.load_model()

    def load_model(self) -> bool:
        """Load trained Maharashtra crop model."""
        if os.path.exists(self.model_path):
            try:
                self.model_payload = joblib.load(self.model_path)
                logger.info(f"Successfully loaded Maharashtra crop model from {self.model_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to load crop model: {e}")
        else:
            logger.warning(f"Crop model not found at {self.model_path}. Training on Maharashtra dataset...")
            try:
                from train_crop_model import train_maharashtra_model
                train_maharashtra_model()
                if os.path.exists(self.model_path):
                    self.model_payload = joblib.load(self.model_path)
                    return True
            except Exception as e:
                logger.error(f"Auto-train failed: {e}")
        return False

    def predict(
        self,
        n: float,
        p: float,
        k: float,
        temp: float,
        humidity: float,
        ph: float,
        rainfall: float,
        city: Optional[str] = None,
        state: Optional[str] = None,
        district: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Predict best crop tailored to Maharashtra's soil, rainfall, and agro-climatic conditions.
        Integrates verified district-wise empirical datasets and regional reference datasets when available.
        """
        eff_rainfall = rainfall if rainfall >= 300.0 else (rainfall * 4.5)
        features = np.array([[n, p, k, temp, humidity, ph, eff_rainfall]])

        target_dist = district or city or ""
        zone_name = None
        clean_state_input = state.strip().lower() if state and state.strip() else ""
        is_telangana_state = (clean_state_input == "telangana")
        is_ap_state = (clean_state_input in ("andhra pradesh", "ap", "andhra"))
        is_gujarat_state = (clean_state_input in ("gujarat", "gj"))
        is_haryana_state = (clean_state_input in ("haryana", "hr"))
        is_karnataka_state = (clean_state_input in ("karnataka", "ka"))
        is_madhya_pradesh_state = (clean_state_input in ("madhya pradesh", "mp"))
        is_punjab_state = (clean_state_input in ("punjab", "pb"))
        if target_dist:
            c_key = target_dist.lower().strip()
            # Check Andhra Pradesh zones first if state is AP or key in AP map
            if is_ap_state or c_key in ANDHRA_PRADESH_DISTRICT_ZONE_MAP:
                zone_name = ANDHRA_PRADESH_DISTRICT_ZONE_MAP.get(c_key)
                if not zone_name:
                    for k_map, v_map in ANDHRA_PRADESH_DISTRICT_ZONE_MAP.items():
                        if k_map in c_key or c_key in k_map:
                            zone_name = v_map
                            break

            # Check Haryana zones if state is Haryana or key in HR map
            if not zone_name and (is_haryana_state or c_key in HARYANA_DISTRICT_ZONE_MAP):
                zone_name = HARYANA_DISTRICT_ZONE_MAP.get(c_key)
                if not zone_name:
                    for k_map, v_map in HARYANA_DISTRICT_ZONE_MAP.items():
                        if k_map in c_key or c_key in k_map:
                            zone_name = v_map
                            break

            # Check Gujarat zones if state is Gujarat or key in GJ map
            if not zone_name and (is_gujarat_state or c_key in GUJARAT_DISTRICT_ZONE_MAP):
                zone_name = GUJARAT_DISTRICT_ZONE_MAP.get(c_key)
                if not zone_name:
                    for k_map, v_map in GUJARAT_DISTRICT_ZONE_MAP.items():
                        if k_map in c_key or c_key in k_map:
                            zone_name = v_map
                            break

            # Check Telangana zones if state is Telangana or key in TG map
            if not zone_name and (is_telangana_state or c_key in TELANGANA_DISTRICT_ZONE_MAP):
                zone_name = TELANGANA_DISTRICT_ZONE_MAP.get(c_key)
                if not zone_name:
                    for k_map, v_map in TELANGANA_DISTRICT_ZONE_MAP.items():
                        if k_map in c_key or c_key in k_map:
                            zone_name = v_map
                            break

            # Check Madhya Pradesh zones if state is MP or key in MP map
            if not zone_name and (is_madhya_pradesh_state or c_key in MADHYA_PRADESH_DISTRICT_ZONE_MAP):
                zone_name = MADHYA_PRADESH_DISTRICT_ZONE_MAP.get(c_key)
                if not zone_name:
                    for k_map, v_map in MADHYA_PRADESH_DISTRICT_ZONE_MAP.items():
                        if k_map in c_key or c_key in k_map:
                            zone_name = v_map
                            break

            # Check Punjab zones if state is Punjab or key in PB map
            if not zone_name and (is_punjab_state or c_key in PUNJAB_DISTRICT_ZONE_MAP):
                zone_name = PUNJAB_DISTRICT_ZONE_MAP.get(c_key)
                if not zone_name:
                    for k_map, v_map in PUNJAB_DISTRICT_ZONE_MAP.items():
                        if k_map in c_key or c_key in k_map:
                            zone_name = v_map
                            break

            # Check Karnataka zones if state is Karnataka or key in KA map
            if not zone_name and (is_karnataka_state or c_key in KARNATAKA_DISTRICT_ZONE_MAP):
                zone_name = KARNATAKA_DISTRICT_ZONE_MAP.get(c_key)
                if not zone_name:
                    for k_map, v_map in KARNATAKA_DISTRICT_ZONE_MAP.items():
                        if k_map in c_key or c_key in k_map:
                            zone_name = v_map
                            break

            # Check Maharashtra zones if not found in other states
            if not zone_name and not is_telangana_state and not is_ap_state and not is_gujarat_state and not is_haryana_state and not is_karnataka_state and not is_madhya_pradesh_state and not is_punjab_state:
                zone_name = DISTRICT_ZONE_MAP.get(c_key)
                if not zone_name:
                    for k_map, v_map in DISTRICT_ZONE_MAP.items():
                        if k_map in c_key or c_key in k_map:
                            zone_name = v_map
                            break

        # Query regional dataset registry with state context
        dataset_match = DatasetManager.get_instance().find_crop_matches(
            target_dist, n, p, k, ph, rainfall, temp, state=state
        ) if target_dist else {"matched": False}
        is_verified = dataset_match.get("matched", False)
        dataset_used = dataset_match.get("dataset_name", "General Agricultural Benchmark (Maharashtra Benchmark)") if is_verified else "General Agricultural Benchmark (Maharashtra Benchmark)"
        dataset_level = dataset_match.get("dataset_level", "verified_primary") if is_verified else "fallback"
        regional_notes = dataset_match.get("regional_notes") if is_verified else None

        # Alias map for dataset crops to model classes
        crop_alias_to_model = {
            "tur": "pigeonpeas",
            "pigeon pea": "pigeonpeas",
            "pigeon peas": "pigeonpeas",
            "arhar": "pigeonpeas",
            "gram": "chickpea",
            "jowar": "sorghum",
            "sorghum": "sorghum",
            "cotton": "cotton",
            "sugarcane": "sugarcane",
            "soybean": "soybean",
            "wheat": "wheat",
            "rice": "rice",
            "maize": "maize",
            "bajra": "bajra",
            "pearl millet": "bajra",
            "grapes": "grapes",
            "groundnut": "groundnut",
            "banana": "banana",
            "coconut": "coconut",
            "mango": "mango",
            "onion": "onion",
            "tomato": "tomato",
            "vegetables": "tomato"
        }

        if self.model_payload and 'model' in self.model_payload:
            model = self.model_payload['model']
            classes = list(model.classes_)
            top_alternatives = []
            confidence = 0.90
            
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(features)[0].copy()

                # If district dataset matched, apply empirical frequency boosting
                if is_verified and "crop_probabilities" in dataset_match:
                    crop_probs_data = dataset_match["crop_probabilities"]
                    for i, cls in enumerate(classes):
                        c_lower = cls.lower()
                        # Check direct or alias match in verified dataset
                        for ds_crop, weight in crop_probs_data.items():
                            ds_norm = crop_alias_to_model.get(ds_crop.lower(), ds_crop.lower())
                            if ds_norm == c_lower or c_lower in ds_norm:
                                probs[i] *= (1.0 + 2.5 * weight)

                # Apply Andhra Pradesh Agro-Climatic Zone Prior Weighting (ANGRAU / Dr. YSRHU)
                if zone_name == 'North Coastal Andhra Zone':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'rice':
                            probs[i] *= 2.2
                        elif c == 'sugarcane' and n >= 120:
                            probs[i] *= 2.0
                        elif c == 'cashew' and ph <= 6.5:
                            probs[i] *= 2.0
                        elif c == 'groundnut' and p >= 35:
                            probs[i] *= 1.8
                        elif c == 'maize':
                            probs[i] *= 1.7
                elif zone_name == 'Godavari Delta Zone':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'rice':
                            probs[i] *= 2.4
                        elif c == 'banana' and k >= 80:
                            probs[i] *= 2.2
                        elif c == 'coconut':
                            probs[i] *= 2.1
                        elif c == 'sugarcane' and n >= 130:
                            probs[i] *= 2.0
                        elif c == 'maize':
                            probs[i] *= 1.7
                elif zone_name == 'Krishna Delta & Chili Belt Zone':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'cotton' and n >= 70:
                            probs[i] *= 2.3
                        elif c == 'rice':
                            probs[i] *= 2.1
                        elif c == 'maize':
                            probs[i] *= 1.9
                        elif c in ('chickpea', 'gram'):
                            probs[i] *= 1.8
                        elif c in ('pigeonpeas', 'pigeon peas', 'tur'):
                            probs[i] *= 1.8
                elif zone_name == 'Southern Andhra Zone':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'groundnut' and p >= 35:
                            probs[i] *= 2.3
                        elif c == 'tomato':
                            probs[i] *= 2.1
                        elif c == 'rice' and eff_rainfall >= 600:
                            probs[i] *= 2.0
                        elif c == 'mango':
                            probs[i] *= 1.9
                        elif c in ('pigeonpeas', 'pigeon peas', 'tur'):
                            probs[i] *= 1.8
                elif zone_name == 'Scarce Rainfall Zone of Rayalaseema':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'groundnut' and p >= 35:
                            probs[i] *= 2.4
                        elif c in ('chickpea', 'gram'):
                            probs[i] *= 2.2
                        elif c == 'cotton' and n >= 70:
                            probs[i] *= 2.0
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 2.0
                        elif c in ('pigeonpeas', 'pigeon peas', 'tur'):
                            probs[i] *= 1.8

                # Apply Haryana Agro-Climatic Zone Prior Weighting (CCS HAU Hisar)
                elif zone_name == 'Eastern Agrozone (Yamuna Basin - CCS HAU)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'wheat' and temp < 30:
                            probs[i] *= 2.3
                        elif c == 'rice' and eff_rainfall >= 550:
                            probs[i] *= 2.3
                        elif c == 'sugarcane' and n >= 120:
                            probs[i] *= 2.1
                        elif c == 'mustard' and temp < 28:
                            probs[i] *= 1.9
                        elif c == 'potato':
                            probs[i] *= 1.8
                        elif c == 'maize':
                            probs[i] *= 1.7
                elif zone_name == 'Western Semi-Arid Zone (CCS HAU Hisar)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'cotton' and n >= 70:
                            probs[i] *= 2.4
                        elif c == 'wheat' and temp < 30:
                            probs[i] *= 2.2
                        elif c == 'bajra' and eff_rainfall < 700:
                            probs[i] *= 2.1
                        elif c == 'mustard':
                            probs[i] *= 2.0
                        elif c in ('chickpea', 'gram') and p >= 35:
                            probs[i] *= 1.9
                elif zone_name == 'Southern Arid & NCR Zone (CCS HAU Bawal)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'mustard' and temp < 28:
                            probs[i] *= 2.3
                        elif c == 'bajra':
                            probs[i] *= 2.2
                        elif c == 'wheat' and temp < 30:
                            probs[i] *= 2.0
                        elif c in ('chickpea', 'gram'):
                            probs[i] *= 1.9
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 1.8

                # Apply Gujarat Agro-Climatic Zone Prior Weighting (AAU / JAU / NAU / SDAU)
                elif zone_name == 'Middle Gujarat Zone (AAU Anand)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'cotton' and n >= 70:
                            probs[i] *= 2.2
                        elif c == 'rice' and eff_rainfall >= 500:
                            probs[i] *= 2.1
                        elif c == 'maize':
                            probs[i] *= 2.0
                        elif c == 'banana' and k >= 80:
                            probs[i] *= 2.0
                        elif c == 'tomato':
                            probs[i] *= 1.8
                        elif c in ('pigeonpeas', 'tur'):
                            probs[i] *= 1.7
                elif zone_name == 'Saurashtra & Coastal Zone (JAU Junagadh)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'groundnut' and p >= 35:
                            probs[i] *= 2.4
                        elif c == 'cotton' and n >= 70:
                            probs[i] *= 2.2
                        elif c == 'wheat' and eff_rainfall < 750 and temp < 30:
                            probs[i] *= 2.0
                        elif c in ('chickpea', 'gram'):
                            probs[i] *= 1.9
                        elif c == 'pomegranate' and ph >= 7.2:
                            probs[i] *= 1.8
                elif zone_name == 'North Gujarat & Arid Zone (SDAU)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'bajra':
                            probs[i] *= 2.3
                        elif c == 'groundnut' and p >= 35:
                            probs[i] *= 2.1
                        elif c == 'wheat' and temp < 30:
                            probs[i] *= 2.0
                        elif c == 'cotton' and n >= 65:
                            probs[i] *= 1.9
                        elif c == 'maize':
                            probs[i] *= 1.8
                elif zone_name == 'South Gujarat Heavy Rainfall Zone (NAU Navsari)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'sugarcane' and n >= 120:
                            probs[i] *= 2.4
                        elif c == 'rice':
                            probs[i] *= 2.2
                        elif c == 'mango':
                            probs[i] *= 2.1
                        elif c == 'banana' and k >= 80:
                            probs[i] *= 2.0
                        elif c in ('pigeonpeas', 'tur'):
                            probs[i] *= 1.8

                # Apply Telangana Agro-Climatic Zone Prior Weighting (PJTSAU)
                elif zone_name == 'Northern Telangana Zone':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'cotton' and n >= 70:
                            probs[i] *= 2.2
                        elif c == 'soybean' and p >= 35:
                            probs[i] *= 2.1
                        elif c == 'rice':
                            probs[i] *= 2.0
                        elif c == 'maize':
                            probs[i] *= 1.8
                        elif c in ('pigeonpeas', 'pigeon peas'):
                            probs[i] *= 1.8
                elif zone_name == 'Central Telangana Zone':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'cotton' and n >= 70:
                            probs[i] *= 2.3
                        elif c == 'rice':
                            probs[i] *= 2.1
                        elif c == 'maize':
                            probs[i] *= 1.8
                        elif c in ('pigeonpeas', 'pigeon peas'):
                            probs[i] *= 1.8
                elif zone_name == 'Southern Telangana Zone':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'rice' and eff_rainfall >= 500:
                            probs[i] *= 2.2
                        elif c == 'cotton' and n >= 70:
                            probs[i] *= 2.0
                        elif c in ('pigeonpeas', 'pigeon peas'):
                            probs[i] *= 2.0
                        elif c == 'groundnut' and p >= 35:
                            probs[i] *= 2.0
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 1.8

                # Apply Punjab Agro-Climatic Zone Prior Weighting (PAU Ludhiana)
                elif zone_name == 'Central Plain Zone (Rice-Wheat)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'wheat' and temp < 30:
                            probs[i] *= 2.5
                        elif c == 'rice' and eff_rainfall >= 450:
                            probs[i] *= 2.4
                        elif c == 'maize':
                            probs[i] *= 1.9
                        elif c == 'potato':
                            probs[i] *= 1.8
                        elif c == 'sugarcane' and n >= 130:
                            probs[i] *= 1.7
                elif zone_name == 'South-Western Semi-Arid Zone (Cotton-Wheat)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'cotton' and n >= 70:
                            probs[i] *= 2.5
                        elif c == 'wheat' and temp < 30:
                            probs[i] *= 2.2
                        elif c == 'mustard':
                            probs[i] *= 2.0
                        elif c in ('chickpea', 'gram'):
                            probs[i] *= 1.9
                        elif c == 'bajra':
                            probs[i] *= 1.8
                elif zone_name == 'Sub-Mountain Undulating Zone (Kandi)':
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'maize':
                            probs[i] *= 2.4
                        elif c == 'wheat' and temp < 30:
                            probs[i] *= 2.2
                        elif c == 'sugarcane' and n >= 120:
                            probs[i] *= 1.8
                        elif c == 'mustard':
                            probs[i] *= 1.7

                # Apply Maharashtra Agro-Climatic Zone Prior Weighting
                elif zone_name == 'Central Vidarbha Zone':
                    # Yavatmal, Wardha, Nagpur, Akola, Amravati, Buldhana, Washim
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'cotton' and n >= 70:
                            probs[i] *= 2.2
                        elif c == 'soybean' and p >= 35:
                            probs[i] *= 2.0
                        elif c in ('pigeonpeas', 'pigeon peas') and p >= 40:
                            probs[i] *= 1.9
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 1.8
                        elif c == 'orange' and 20 <= n <= 60 and 20 <= p <= 45:
                            probs[i] *= 1.8
                        elif c == 'chickpea' and temp <= 26.0:
                            probs[i] *= 1.7
                        elif c in ('rice', 'jute') and eff_rainfall < 1300:
                            probs[i] = 0.0

                elif zone_name == 'Central Maharashtra (Marathwada)':
                    # Latur, Nanded, Beed, Jalna, Sambhajinagar, Parbhani
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'soybean' and p >= 35:
                            probs[i] *= 2.2
                        elif c == 'cotton' and n >= 70:
                            probs[i] *= 2.0
                        elif c in ('pigeonpeas', 'pigeon peas'):
                            probs[i] *= 2.0
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 1.8
                        elif c == 'sweet_lime':
                            probs[i] *= 1.7
                        elif c == 'sugarcane' and n >= 140:
                            probs[i] *= 1.6

                elif zone_name == 'Khandesh & Tapi Basin':
                    # Jalgaon, Dhule, Nandurbar
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'banana' and k >= 80 and n >= 100:
                            probs[i] *= 2.5
                        elif c == 'cotton' and n >= 75:
                            probs[i] *= 2.0
                        elif c == 'maize':
                            probs[i] *= 1.8
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 1.7

                elif zone_name in ('South Konkan', 'North Konkan'):
                    # Ratnagiri, Sindhudurg, Raigad, Thane
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'mango' and ph <= 7.0:
                            probs[i] *= 2.5
                        elif c == 'cashew' and ph <= 6.5:
                            probs[i] *= 2.4
                        elif c == 'rice':
                            probs[i] *= 2.2
                        elif c == 'coconut':
                            probs[i] *= 2.0

                elif zone_name in ('Western Maharashtra Plain', 'Scarcity & Rain Shadow Zone'):
                    # Kolhapur, Sangli, Pune, Satara, Solapur, Ahmednagar, Nashik
                    for i, cls in enumerate(classes):
                        c = cls.lower()
                        if c == 'sugarcane' and n >= 130 and eff_rainfall >= 850:
                            probs[i] *= 2.3
                        elif c == 'grapes' and k >= 100 and p >= 70:
                            probs[i] *= 2.4
                        elif c == 'onion' and 50 <= n <= 110:
                            probs[i] *= 2.2
                        elif c == 'pomegranate' and ph >= 7.0:
                            probs[i] *= 2.2
                        elif c in ('sorghum', 'jowar'):
                            probs[i] *= 2.0

                # Renormalize probabilities
                total_p = np.sum(probs)
                if total_p > 0:
                    probs = probs / total_p

                top_indices = np.argsort(probs)[::-1]
                pred_class = classes[top_indices[0]]
                confidence = round(float(probs[top_indices[0]]), 4)
                
                for idx in top_indices[1:4]:
                    if probs[idx] > 0.04:
                        top_alternatives.append({
                            'crop': self._format_crop_name(str(classes[idx])),
                            'probability': round(float(probs[idx]), 4)
                        })

                desc = self._generate_description(
                    pred_class,
                    target_dist.title() if target_dist else (zone_name or "Maharashtra Agricultural Zone"),
                    is_verified,
                    dataset_used,
                    dataset_level
                )

                return {
                    'crop': self._format_crop_name(str(pred_class)),
                    'confidence': confidence,
                    'top_alternatives': top_alternatives,
                    'model_used': f"RandomForestClassifier + {dataset_used}" if is_verified else 'RandomForestClassifier (Maharashtra Agricultural Benchmark)',
                    'agro_climatic_zone': zone_name or 'Maharashtra State Agrozones',
                    'description': desc,
                    'state': self._resolve_state(state, dataset_match.get('state'), zone_name),
                    'district': target_dist.strip().title() if target_dist else None,
                    'dataset_used': dataset_used,
                    'dataset_level': dataset_level,
                    'is_district_verified': is_verified,
                    'zinc_target': dataset_match.get("zinc_target"),
                    'sulphur_target': dataset_match.get("sulphur_target"),
                    'regional_notes': regional_notes
                }

        # Fallback
        return self._heuristic_fallback(n, p, k, temp, humidity, ph, eff_rainfall, zone_name, target_dist, state, is_verified, dataset_used, dataset_level, regional_notes, dataset_match)

    def _format_crop_name(self, crop: str) -> str:
        """Friendly names with regional/Marathi names."""
        c = crop.lower().strip()
        return CROP_DISPLAY_NAMES.get(c, crop.capitalize())

    def _generate_description(
        self,
        crop: str,
        zone: str,
        is_verified: bool = False,
        dataset_name: Optional[str] = None,
        dataset_level: str = "verified_primary"
    ) -> str:
        name = self._format_crop_name(crop)
        if is_verified and dataset_name:
            if dataset_level == "verified_primary":
                return (
                    f"Verified Recommendation ({dataset_name}): Based on empirical field trials in {zone}, "
                    f"soil macronutrients (N-P-K), soil pH, and rainfall, {name} demonstrates highest suitability and yield resilience."
                )
            else:
                return (
                    f"Regional Reference Recommendation ({dataset_name}): Based on state agronomic benchmarks, "
                    f"soil nutrient targets (N-P-K, pH), and agro-climatic conditions of {zone}, {name} is recommended for optimal yield."
                )
        return (
            f"Based on soil macronutrients (N-P-K), soil pH, rainfall, and agro-climatic conditions of {zone}, "
            f"{name} is highly recommended for optimal yield and economic profitability in Maharashtra."
        )

    def _heuristic_fallback(
        self,
        n: float,
        p: float,
        k: float,
        temp: float,
        humidity: float,
        ph: float,
        rainfall: float,
        zone: Optional[str],
        target_dist: Optional[str] = None,
        state: Optional[str] = None,
        is_verified: bool = False,
        dataset_used: Optional[str] = None,
        dataset_level: str = "fallback",
        regional_notes: Optional[str] = None,
        dataset_match: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Agronomic fallback specifically for Maharashtra."""
        if zone == 'Central Vidarbha Zone' or (550 <= rainfall <= 1250 and 22 <= temp <= 38 and ph >= 6.5):
            if n >= 80:
                crop = "Cotton (Bt Cotton / Kapas)"
            elif p >= 45 and n <= 50:
                crop = "Soybean (Soya)"
            elif 55 <= n <= 85:
                crop = "Sorghum (Jowar / Maldandi)"
            else:
                crop = "Pigeon Pea (Tur / Arhar)"
        elif rainfall > 1800:
            crop = "Rice (Paddy / Bhat)" if humidity > 75 else "Mango (Alphonso / Hapus)"
        elif k > 100 and p > 70:
            crop = "Grapes (Draksha)"
        elif rainfall < 600 and ph >= 7.2:
            crop = "Pomegranate (Dalimb - Bhagwa)"
        else:
            crop = "Soybean (Soya)"

        zn_target = dataset_match.get("zinc_target") if dataset_match else None
        s_target = dataset_match.get("sulphur_target") if dataset_match else None

        return {
            'crop': crop,
            'confidence': 0.88,
            'top_alternatives': [
                {'crop': 'Cotton (Bt Cotton / Kapas)', 'probability': 0.40},
                {'crop': 'Soybean (Soya)', 'probability': 0.35},
                {'crop': 'Pigeon Pea (Tur / Arhar)', 'probability': 0.25}
            ],
            'model_used': f"AgronomicRuleEngine + {dataset_used}" if is_verified else 'AgronomicRuleEngine (Maharashtra Fallback)',
            'agro_climatic_zone': zone or 'Maharashtra Agrozone',
            'description': (
                "Recommended for Punjab based on PAU Ludhiana agronomic parameters." if (state == 'Punjab' or any(pb_kw in (zone or '') for pb_kw in ['Punjab', 'Central Plain', 'South-Western', 'Kandi', 'PAU']))
                else "Recommended for Madhya Pradesh based on JNKVV/RVSKVV agronomic parameters." if (state == 'Madhya Pradesh' or any(mp_kw in (zone or '') for mp_kw in ['Madhya Pradesh', 'Malwa', 'Nimar', 'Gird', 'Narmada', 'Bundelkhand', 'Vindhyan', 'JNKVV', 'RVSKVV']))
                else "Recommended for Karnataka based on UAS Bangalore/Dharwad/Shivamogga agronomic parameters." if (state == 'Karnataka' or any(ka_kw in (zone or '') for ka_kw in ['Karnataka', 'Malnad', 'KSNUAHS', 'UAS Bangalore', 'UAS Dharwad']))
                else "Recommended for Andhra Pradesh based on ANGRAU/Dr. YSRHU agronomic parameters." if (state == 'Andhra Pradesh' or any(ap_kw in (zone or '') for ap_kw in ['Andhra', 'Rayalaseema', 'Godavari', 'Krishna']))
                else "Recommended for Telangana based on PJTSAU agronomic parameters." if (state == 'Telangana' or 'Telangana' in (zone or ''))
                else "Recommended for Maharashtra based on state agricultural university parameters."
            ),
            'state': self._resolve_state(state, dataset_match.get('state') if dataset_match else None, zone),
            'district': target_dist.strip().title() if target_dist else None,
            'dataset_used': dataset_used or 'General Agricultural Benchmark',
            'dataset_level': dataset_level,
            'is_district_verified': is_verified,
            'zinc_target': zn_target,
            'sulphur_target': s_target,
            'regional_notes': regional_notes
        }
