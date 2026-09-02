"""
Integration test for AgriDisha services including Email OTP Verification.
"""
import requests
import re
import subprocess

def test_system():
    print("1. Testing ML Service Crop Predict...")
    crop_payload = {
        "nitrogen": 90.0,
        "phosphorous": 42.0,
        "potassium": 43.0,
        "temperature": 28.5,
        "humidity": 78.0,
        "ph": 6.5,
        "rainfall": 200.0
    }
    r = requests.post("http://localhost:8000/api/ml/crop-predict", json=crop_payload)
    print(f"ML Crop Predict Status: {r.status_code}, Response: {r.json()}")

    print("\n2. Testing Spring Boot Backend Weather API...")
    r = requests.get("http://localhost:8080/api/weather/Mumbai")
    print(f"Weather API Status: {r.status_code}, Response: {r.json()}")

    print("\n3. Testing Spring Boot Backend Crop Recommendation API...")
    backend_crop_req = {
        "nitrogen": 90.0,
        "phosphorous": 42.0,
        "potassium": 43.0,
        "ph": 6.5,
        "rainfall": 200.0,
        "city": "Mumbai"
    }
    r = requests.post("http://localhost:8080/api/crop/recommend", json=backend_crop_req)
    print(f"Backend Crop Recommend Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Crop Recommend Response: {r.json()}")
    else:
        print(f"Crop Recommend Error: {r.text}")

    print("\n4. Testing Spring Boot Backend Fertilizer Recommendation API...")
    fert_req = {
        "cropName": "Rice",
        "nitrogen": 25.0,
        "phosphorous": 40.0,
        "potassium": 40.0
    }
    r = requests.post("http://localhost:8080/api/fertilizer/recommend", json=fert_req)
    print(f"Backend Fertilizer Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Fertilizer Response: {r.json()}")
    else:
        print(f"Fertilizer Error: {r.text}")

    print("\n5. Testing Spring Boot 2-Step Registration with Email OTP Verification...")
    otp_user = {
        "username": "farmer_suresh",
        "email": "suresh@agridisha.com",
        "password": "strongPassword123",
        "fullName": "Suresh Deshmukh",
        "location": "Nagpur, Maharashtra"
    }
    r_otp = requests.post("http://localhost:8080/api/auth/send-otp", json=otp_user)
    print(f"Send OTP Status: {r_otp.status_code}, Response: {r_otp.json()}")

    # Retrieve OTP from container logs
    log_output = subprocess.check_output(['docker', 'logs', 'agridisha-backend'], text=True, errors='ignore')
    matches = re.findall(r'Generated 6-digit OTP \[([0-9]{6})\] for email: suresh@agridisha.com', log_output)
    if matches:
        otp = matches[-1]
        print(f"Retrieved Generated OTP: {otp}")
        r_verify = requests.post("http://localhost:8080/api/auth/verify-otp-register", json={"email": "suresh@agridisha.com", "otp": otp})
        print(f"Verify OTP & Register Status: {r_verify.status_code}, Response: {r_verify.json()}")
        token = r_verify.json().get('token')
        if token:
            r_profile = requests.get("http://localhost:8080/api/users/profile", headers={"Authorization": f"Bearer {token}"})
            print(f"Authenticated Profile Status: {r_profile.status_code}, User: {r_profile.json().get('fullName')}")

if __name__ == "__main__":
    test_system()
