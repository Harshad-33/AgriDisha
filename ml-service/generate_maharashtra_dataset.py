"""
Maharashtra Specific Agricultural Dataset Generator.
Based on ICAR, MPKV Rahuri, Dr. PDKV Akola, VNMKV Parbhani, and BSKKV Dapoli benchmarks.
Covers authentic N, P, K, pH, Temperature, Humidity, and Rainfall patterns across all regions of Maharashtra.
"""
import os
import numpy as np
import pandas as pd

# Authentic agronomic profiles for Maharashtra crops:
# (N_min, N_max, P_min, P_max, K_min, K_max, temp_min, temp_max, hum_min, hum_max, ph_min, ph_max, rain_min, rain_max)
MAHARASHTRA_CROP_PROFILES = {
    # 1. Cotton (Bt Cotton / Kapas) - Vidarbha (Yavatmal, Wardha, Akola, Amravati), Marathwada, Khandesh (Jalgaon)
    'cotton': (85, 150, 35, 70, 15, 38, 24.0, 38.0, 42.0, 72.0, 6.8, 8.6, 650.0, 1150.0),

    # 2. Soybean (Soya) - Vidarbha, Marathwada (Latur, Nanded), Western MH (Kolhapur, Sangli)
    'soybean': (20, 50, 40, 75, 20, 45, 22.0, 34.0, 50.0, 75.0, 6.0, 7.8, 650.0, 1100.0),

    # 3. Pigeon Pea (Tur / Arhar) - Vidarbha (Yavatmal), Marathwada (Latur, Osmanabad)
    'pigeonpeas': (15, 45, 50, 80, 15, 35, 24.0, 38.0, 40.0, 70.0, 6.0, 8.2, 600.0, 1050.0),

    # 4. Sorghum (Jowar / Maldandi) - Solapur, Ahmednagar, Marathwada, Vidarbha
    'sorghum': (55, 95, 25, 50, 25, 48, 24.0, 38.0, 35.0, 65.0, 6.5, 8.5, 450.0, 800.0),

    # 5. Chickpea (Gram / Harbara) - Post-monsoon Rabi crop across Maharashtra
    'chickpea': (20, 45, 45, 75, 50, 75, 16.0, 26.0, 18.0, 45.0, 6.2, 8.4, 400.0, 750.0),

    # 6. Sugarcane (Oos) - Western Maharashtra (Kolhapur, Pune, Satara, Sangli, Ahmednagar)
    'sugarcane': (150, 250, 60, 95, 80, 130, 22.0, 38.0, 55.0, 85.0, 6.5, 8.2, 900.0, 2200.0),

    # 7. Onion (Kanda) - Nashik (Lasalgaon), Ahmednagar, Pune, Solapur
    'onion': (60, 110, 40, 65, 40, 70, 18.0, 32.0, 45.0, 70.0, 6.0, 7.8, 500.0, 850.0),

    # 8. Grapes (Draksha) - Nashik, Sangli (Tasgaon), Solapur, Pune
    'grapes': (20, 50, 80, 120, 120, 180, 14.0, 35.0, 40.0, 70.0, 6.5, 8.0, 500.0, 800.0),

    # 9. Pomegranate (Dalimb - Bhagwa) - Solapur, Ahmednagar, Sangli, Beed, Nashik
    'pomegranate': (25, 55, 20, 45, 40, 75, 20.0, 38.0, 30.0, 65.0, 6.5, 8.4, 450.0, 750.0),

    # 10. Banana (Keli - Grand Naine) - Jalgaon (Banana Capital), Solapur, Nanded
    'banana': (120, 200, 50, 90, 100, 180, 24.0, 38.0, 60.0, 85.0, 6.0, 7.8, 800.0, 1500.0),

    # 11. Orange (Nagpur Mandarin / Santra) - Nagpur, Amravati (Morshi/Warud)
    'orange': (25, 60, 20, 45, 30, 60, 20.0, 38.0, 40.0, 70.0, 6.5, 8.0, 750.0, 1100.0),

    # 12. Sweet Lime (Mosambi) - Jalna, Chhatrapati Sambhajinagar, Nanded
    'sweet_lime': (30, 65, 20, 45, 35, 65, 22.0, 38.0, 40.0, 68.0, 6.5, 8.2, 650.0, 950.0),

    # 13. Mango (Alphonso / Hapus) - Konkan (Ratnagiri, Sindhudurg - Devgad)
    'mango': (20, 50, 15, 35, 30, 55, 22.0, 35.0, 65.0, 88.0, 5.5, 7.2, 2000.0, 3500.0),

    # 14. Cashew (Kaju) - Konkan (Sindhudurg - Vengurla, Ratnagiri)
    'cashew': (20, 50, 15, 30, 20, 40, 22.0, 36.0, 60.0, 88.0, 5.0, 6.5, 1800.0, 3600.0),

    # 15. Rice (Paddy / Bhat) - Konkan (Ratnagiri, Raigad, Thane, Palghar) & Eastern Vidarbha (Bhandara, Gondia)
    'rice': (70, 110, 35, 60, 35, 55, 22.0, 34.0, 75.0, 92.0, 5.5, 7.5, 1200.0, 3500.0),

    # 16. Wheat (Gahu - Sharbati/Lokwan) - Rabi crop across irrigated Maharashtra (Nashik, Pune, Vidarbha)
    'wheat': (80, 120, 40, 65, 30, 50, 14.0, 26.0, 35.0, 65.0, 6.5, 8.0, 400.0, 750.0),

    # 17. Maize (Makka) - Nashik, Jalgaon, Aurangabad, Sangli
    'maize': (80, 130, 40, 65, 30, 55, 18.0, 32.0, 45.0, 72.0, 5.8, 7.4, 500.0, 850.0),

    # 18. Pearl Millet (Bajra) - Scarcity & Rain shadow zones (Beed, Ahmednagar, Dhule, Jalna)
    'bajra': (40, 80, 20, 45, 20, 40, 24.0, 38.0, 30.0, 60.0, 6.5, 8.5, 350.0, 650.0),

    # 19. Finger Millet (Nachani / Ragi) - Konkan hills and Western Ghats slopes
    'ragi': (30, 60, 20, 40, 20, 40, 20.0, 32.0, 65.0, 88.0, 5.2, 6.8, 1200.0, 3200.0),

    # 20. Groundnut (Bhuimug) - Khandesh, Marathwada, Western Maharashtra
    'groundnut': (20, 45, 40, 70, 30, 55, 22.0, 34.0, 45.0, 70.0, 6.0, 7.5, 500.0, 850.0),

    # 21. Tomato - Nashik, Pune (Narayangaon, Junnar), Ahmednagar
    'tomato': (90, 140, 50, 80, 60, 110, 18.0, 32.0, 50.0, 75.0, 6.0, 7.5, 550.0, 950.0),

    # 22. Coconut (Naral) - Konkan Coast
    'coconut': (30, 60, 20, 40, 60, 120, 24.0, 34.0, 70.0, 90.0, 5.5, 7.5, 1500.0, 3500.0)
}


def generate_maharashtra_dataset(samples_per_crop: int = 300, seed: int = 42) -> pd.DataFrame:
    """Generate high-fidelity Maharashtra agricultural dataset."""
    np.random.seed(seed)
    rows = []

    for crop, (n_min, n_max, p_min, p_max, k_min, k_max, t_min, t_max, h_min, h_max, ph_min, ph_max, r_min, r_max) in MAHARASHTRA_CROP_PROFILES.items():
        n = np.random.uniform(n_min * 0.94, n_max * 1.06, samples_per_crop)
        p = np.random.uniform(p_min * 0.94, p_max * 1.06, samples_per_crop)
        k = np.random.uniform(k_min * 0.94, k_max * 1.06, samples_per_crop)
        temp = np.random.uniform(t_min * 0.96, t_max * 1.04, samples_per_crop)
        hum = np.clip(np.random.uniform(h_min * 0.96, min(95.0, h_max * 1.04), samples_per_crop), 15.0, 98.0)
        ph = np.clip(np.random.uniform(ph_min * 0.98, ph_max * 1.02, samples_per_crop), 4.5, 9.0)
        rain = np.clip(np.random.uniform(r_min * 0.92, r_max * 1.08, samples_per_crop), 250.0, 4200.0)

        for i in range(samples_per_crop):
            rows.append({
                'N': round(float(n[i]), 2),
                'P': round(float(p[i]), 2),
                'K': round(float(k[i]), 2),
                'temperature': round(float(temp[i]), 2),
                'humidity': round(float(hum[i]), 2),
                'ph': round(float(ph[i]), 2),
                'rainfall': round(float(rain[i]), 2),
                'label': crop
            })

    df = pd.DataFrame(rows)
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "maharashtra_crop_data.csv")
    df = generate_maharashtra_dataset(samples_per_crop=300)
    df.to_csv(out_file, index=False)
    print(f"Successfully generated {out_file} with {len(df)} records across {len(MAHARASHTRA_CROP_PROFILES)} authentic Maharashtra crops.")
