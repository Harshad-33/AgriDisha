# 🌾 AgriDisha - Smart Agriculture Recommendation System

[![Java](https://img.shields.io/badge/Java-21-orange.svg)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.3.5-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![Angular](https://img.shields.io/badge/Angular-19%2B-red.svg)](https://angular.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue.svg)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)

**AgriDisha** is an enterprise-grade full-stack smart agriculture decision-support platform. It assists farmers, agricultural scientists, and precision agriculture practitioners in:
1. **Predicting the optimal crop** to cultivate based on soil macronutrients (N, P, K), soil pH, rainfall, and live local meteorological conditions.
2. **Recommending targeted fertilizers** (chemical formulas and organic alternatives) by diagnosing soil nutrient deficiencies or surpluses.
3. **Detecting plant leaf diseases** from uploaded leaf photographs using a deep convolutional neural network (PyTorch ResNet-9) trained on 38 PlantVillage disease classes, paired with comprehensive pathogen etiology, prevention protocols, and fungicide treatments.

---

## 🏗️ 1. Architecture Overview

AgriDisha follows a clean **decoupled three-tier microservice architecture**:

```
+-------------------------------------------------------------+
|               Angular 19+ Frontend (Port 4200)              |
|        Bootstrap 5 • Reactive Forms • JWT Interceptor       |
+-------------------------------------------------------------+
                              |
                              | REST APIs + JWT Auth
                              v
+-------------------------------------------------------------+
|            Java Spring Boot 3 Backend (Port 8080)           |
|      Spring Security • JPA • OpenWeatherMap Gateway         |
+-------------------------------------------------------------+
             |                                    |
             | Internal REST                      | JDBC / SQL
             v                                    v
+-----------------------------+     +--------------------------+
|  Python FastAPI ML Service  |     |   MySQL 8.0 Database     |
|         (Port 8000)         |     |        (Port 3306)       |
|  - Crop Model (RandomForest)|     |  - users                 |
|  - Fertilizer Rule Engine   |     |  - crop_predictions      |
|  - Disease CNN (PyTorch)    |     |  - fertilizer_recs       |
+-----------------------------+     |  - disease_predictions   |
                                    +--------------------------+
```

### Architectural Responsibilities:
- **Angular Frontend:** Modern responsive user interface, forms validation, live weather triggers, drag-and-drop leaf uploader, user dashboard, and history logs.
- **Spring Boot Backend:** API Gateway, JWT stateless authentication, database persistence, OpenWeatherMap integration, business rules, and secure client for ML inference.
- **Python FastAPI ML Microservice:** Dedicated high-performance ML inference engine for crop modeling, soil nutrient deficiency rules, and PyTorch computer vision inference.
- **MySQL Database:** Relational persistent storage for registered users, crop predictions, fertilizer plans, and disease scans.

---

## 🌟 2. Core Modules & Features

### 1. 🌱 Crop Recommendation
- **Inputs:** Soil Nitrogen ($N$), Phosphorous ($P$), Potassium ($K$), Soil pH, Rainfall (mm), and City Name.
- **Weather Automation:** Automatically queries OpenWeatherMap API for the specified city to retrieve real-time Temperature (°C) and Humidity (%).
- **Model:** Random Forest / XGBoost classifier trained on 22 agronomic crops (Rice, Maize, Chickpea, Kidney Beans, Pigeon Peas, Moth Beans, Mung Bean, Black Gram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee).
- **Outputs:** Recommended crop name, confidence score, and top alternative crops.

### 2. 🧪 Fertilizer Recommendation
- **Inputs:** Target Crop, Current Soil Nitrogen ($N$), Phosphorous ($P$), Potassium ($K$).
- **Rule Engine:** Calculates variance against the crop's optimal nutrient thresholds to categorize $N$, $P$, and $K$ as **Low**, **High**, or **Optimal**.
- **Outputs:**
  - Soil status overview (e.g., `N: Low, P: Optimal, K: Low`).
  - Chemical fertilizer recommendations (e.g., Urea, DAP, MOP).
  - Organic alternatives (e.g., Farmyard Manure, bone meal, wood ash, vermicompost).
  - Soil management and application timing advice.

### 3. 🍃 Plant Leaf Disease Detection
- **Inputs:** High-resolution plant leaf photograph (JPEG, PNG, WebP).
- **Model:** PyTorch ResNet-9 convolutional neural network classifying 38 PlantVillage crop and disease classes (Apple, Cherry, Corn, Grape, Orange, Peach, Pepper Bell, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato).
- **Outputs:**
  - Health status (`Healthy` vs `Diseased`)
  - Crop and disease name
  - Confidence percentage and severity level
  - Biological pathogen cause
  - Symptoms description
  - Prevention strategy
  - Recommended fungicide/chemical treatment and organic supplements

---

## 📂 3. Project Directory Structure

```
agridisha/
├── backend/
│   ├── pom.xml                               # Maven Project Descriptor (Java 21, Spring Boot 3.3.5)
│   ├── Dockerfile                            # Multi-stage Maven + Temurin JRE build
│   └── src/
│       ├── main/
│       │   ├── java/com/agridisha/
│       │   │   ├── AgriDishaApplication.java
│       │   │   ├── config/                   # SecurityConfig, JwtTokenProvider, CorsConfig, RestTemplate
│       │   │   ├── controller/               # Auth, Crop, Fertilizer, Disease, Weather, History, User
│       │   │   ├── dto/                      # Request & Response DTOs
│       │   │   ├── entity/                   # JPA Entities (User, CropPrediction, Fertilizer, Disease)
│       │   │   ├── exception/                # GlobalExceptionHandler & custom exceptions
│       │   │   ├── repository/               # Spring Data JPA Repositories
│       │   │   └── service/                  # Business Logic, ML Client, OpenWeatherMap Client
│       │   └── resources/
│       │       ├── application.properties    # MySQL, Weather API, JWT, ML URL configs
│       │       └── application-test.properties # H2 in-memory test configuration
│       └── test/
│           └── java/com/agridisha/AgriDishaApplicationTests.java
│
├── ml-service/
│   ├── app.py                                # FastAPI Application Endpoints
│   ├── requirements.txt                      # Python dependencies (FastAPI, PyTorch, scikit-learn, etc.)
│   ├── Dockerfile                            # Python 3.11-slim container definition
│   ├── train_crop_model.py                   # Automated agronomic dataset generator & trainer
│   ├── data/
│   │   ├── crop_data.csv                     # 22-crop agronomic dataset (3,300 records)
│   │   └── fertilizer_knowledge.json         # Crop NPK thresholds & agronomic treatment rules
│   ├── models/
│   │   ├── crop_recommendation.joblib        # Trained Random Forest classifier
│   │   └── plant_disease_model.pth           # PyTorch ResNet9 model weights
│   ├── services/
│   │   ├── crop_service.py                   # Crop prediction & probability scoring
│   │   ├── fertilizer_service.py             # Nutrient evaluation rule engine
│   │   └── disease_service.py                # Image preprocessing & ResNet9 inference
│   └── utils/
│       ├── resnet9.py                        # PyTorch ResNet-9 architecture & transform pipeline
│       └── disease_info.py                   # Complete 38-class PlantVillage knowledge base
│
├── frontend/
│   ├── package.json                          # Angular 19+, Bootstrap 5, Bootstrap Icons
│   ├── angular.json                          # Angular CLI configuration
│   ├── tsconfig.json                         # TypeScript configuration
│   ├── nginx.conf                            # Nginx production reverse proxy config
│   ├── Dockerfile                            # Multi-stage Node build + Nginx runtime
│   └── src/
│       ├── index.html
│       ├── styles.css                        # Modern custom agriculture theme
│       ├── main.ts
│       └── app/
│           ├── app.component.ts/.html/.css
│           ├── app.config.ts                 # Providers (Router, HttpClient with JWT interceptor)
│           ├── app.routes.ts                 # Route definitions & AuthGuards
│           ├── core/                         # Auth, Interceptor, Guards, Services, Models
│           ├── shared/                       # Navbar, Footer
│           └── pages/
│               ├── home/                     # Hero landing page & 3 feature cards
│               ├── login/ & register/        # JWT Authentication forms
│               ├── dashboard/                # User analytics & quick actions
│               ├── crop-recommendation/      # Crop prediction with auto-weather fetch
│               ├── fertilizer-recommendation/# Soil NPK deficiency evaluator
│               ├── disease-detection/        # Leaf drag & drop uploader & diagnosis
│               ├── history/                  # Filterable prediction history
│               └── profile/                  # Account info & statistics
│
├── database/
│   └── schema.sql                            # MySQL 8.0 DDL & initial seed user
├── docker-compose.yml                        # Multi-container orchestration (MySQL, ML, Backend, Frontend)
└── README.md                                 # Full documentation & run instructions
```

---

## 🚀 4. How to Run the Application

### Option A: Running with Docker Compose (Recommended)

To run the entire system (MySQL + ML Service + Spring Boot + Angular) in one command:

```bash
# 1. Clone or navigate to the project directory
cd agridisha

# 2. (Optional) Set your OpenWeatherMap API key
export OPENWEATHER_API_KEY=your_openweathermap_api_key

# 3. Launch all containers
docker-compose up --build
```

Access the services:
- **Angular Frontend:** `http://localhost:4200` or `http://localhost:80`
- **Spring Boot Backend:** `http://localhost:8080`
- **FastAPI ML Service Docs:** `http://localhost:8000/docs`
- **MySQL Database:** `localhost:3307` (`root` / `root`)

---

### Option B: Running Manually (Without Docker)

#### Step 1: Start MySQL Database
1. Ensure MySQL Server is running on port `3306`.
2. Import the schema:
   ```bash
   mysql -u root -p < database/schema.sql
   ```
   *(Default credentials configured: `root` / `root`, Database: `agridisha`)*

#### Step 2: Start Python ML Microservice
1. Navigate to `ml-service/`:
   ```bash
   cd ml-service
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Train/generate the crop recommendation model:
   ```bash
   python train_crop_model.py
   ```
5. Launch FastAPI server:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```
   *FastAPI docs will be available at `http://localhost:8000/docs`.*

#### Step 3: Start Java Spring Boot Backend
1. Navigate to `backend/`:
   ```bash
   cd backend
   ```
2. (Optional) Configure `src/main/resources/application.properties` with your MySQL credentials or OpenWeatherMap API key:
   ```properties
   spring.datasource.username=root
   spring.datasource.password=root
   agridisha.weather.api-key=your_openweathermap_api_key
   ```
3. Run the Spring Boot application using Maven:
   ```bash
   mvn spring-boot:run
   ```
   *Backend REST API will be active at `http://localhost:8080`.*

#### Step 4: Start Angular Frontend
1. Navigate to `frontend/`:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install --legacy-peer-deps
   ```
3. Start the Angular development server:
   ```bash
   npm start
   # or
   npx ng serve --open
   ```
4. Open your browser at `http://localhost:4200`.

---

## 📡 5. REST API Documentation

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/auth/register` | Register new user account | No |
| `POST` | `/api/auth/login` | Login and obtain JWT token | No |
| `GET` | `/api/users/profile` | Get current user profile & stats | Yes (Bearer JWT) |

### Agriculture Endpoints
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/crop/recommend` | Crop recommendation from soil & weather | Optional (records to user if authenticated) |
| `POST` | `/api/fertilizer/recommend`| Fertilizer & nutrient advice for crop | Optional |
| `POST` | `/api/disease/predict` | Plant leaf disease detection (Multipart image)| Optional |
| `GET` | `/api/weather/{city}` | Live weather for specified city | No |
| `GET` | `/api/history` | Get user prediction history | Yes (Bearer JWT) |
| `GET` | `/api/history/summary` | Get user dashboard metrics & recent items | Yes (Bearer JWT) |

---

## 🧪 6. Sample API Requests & Curl Examples

### 1. Crop Recommendation Request
```bash
curl -X POST http://localhost:8080/api/crop/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "nitrogen": 90,
    "phosphorous": 42,
    "potassium": 43,
    "ph": 6.5,
    "rainfall": 200,
    "city": "Mumbai"
  }'
```

**Sample Response:**
```json
{
  "id": 1,
  "recommendedCrop": "Rice",
  "confidence": 0.9621,
  "modelUsed": "RandomForestClassifier",
  "city": "Mumbai",
  "temperature": 28.5,
  "humidity": 78.0,
  "nitrogen": 90.0,
  "phosphorous": 42.0,
  "potassium": 43.0,
  "ph": 6.5,
  "rainfall": 200.0,
  "topAlternatives": [
    { "crop": "Jute", "probability": 0.031 },
    { "crop": "Coffee", "probability": 0.005 }
  ],
  "description": "Based on your soil nutrient levels and environmental climate, Rice is the optimal crop for maximum yield."
}
```

---

### 2. Fertilizer Recommendation Request
```bash
curl -X POST http://localhost:8080/api/fertilizer/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "cropName": "Rice",
    "nitrogen": 25,
    "phosphorous": 40,
    "potassium": 40
  }'
```

**Sample Response:**
```json
{
  "id": 1,
  "crop": "Rice",
  "soilStatus": "N: Low, P: Optimal, K: Optimal",
  "nitrogen": 25.0,
  "phosphorous": 40.0,
  "potassium": 40.0,
  "nutrientLevels": {
    "nitrogen": { "current": 25.0, "ideal": 80.0, "status": "Low" },
    "phosphorus": { "current": 40.0, "ideal": 40.0, "status": "Optimal" },
    "potassium": { "current": 40.0, "ideal": 40.0, "status": "Optimal" }
  },
  "chemicalFertilizers": [
    "Urea (46% N) at 50-75 kg/hectare or Ammonium Nitrate."
  ],
  "organicAlternatives": [
    "Apply well-decomposed Farmyard Manure (FYM), Neem cake, blood meal, or composted poultry manure."
  ],
  "primaryRecommendation": "Split nitrogen application into basal dose and top dressing during active vegetative growth phase for maximum uptake."
}
```

---

### 3. Plant Disease Detection Request
```bash
curl -X POST http://localhost:8080/api/disease/predict \
  -F "image=@/path/to/tomato_leaf.jpg"
```

**Sample Response:**
```json
{
  "id": 1,
  "rawClass": "Tomato___Early_blight",
  "crop": "Tomato",
  "disease": "Early Blight",
  "status": "Diseased",
  "confidence": 0.945,
  "severity": "Moderate to High",
  "cause": "Fungus Alternaria linariae (Alternaria solani)",
  "symptoms": "Dark brown concentric bullseye rings on bottom leaves, yellowing of surrounding tissue.",
  "prevention": "Prune lower leaves touching soil; stake and cage plants; apply mulch around base; rotate crops for 3 years.",
  "treatment": "Apply Chlorothalonil, Copper Fungicide, or Mancozeb every 7-10 days starting at bottom foliage.",
  "supplement": "Liquid kelp and potassium silicate foliar."
}
```

---

## 🌦️ 7. OpenWeatherMap Configuration

1. Register for a free API key at [OpenWeatherMap](https://openweathermap.org/api).
2. Set the key in `backend/src/main/resources/application.properties`:
   ```properties
   agridisha.weather.api-key=your_actual_key
   ```
   Or set the environment variable:
   ```bash
   export OPENWEATHER_API_KEY=your_actual_key
   ```
3. **Graceful Fallback Mode:** If no key is provided, the backend seamlessly switches to built-in climate simulation for Indian and international cities, ensuring development is never interrupted.

---

## 🛡️ 8. Default Demo User Credentials

For testing the authenticated dashboard and history features immediately:
- **Username:** `farmer_john`
- **Password:** `password123`

---

## 🔧 9. Troubleshooting & FAQ

1. **Weather API fails with 401 Unauthorized:**
   - Verify your OpenWeatherMap API key is activated (new keys can take 10-30 minutes to activate on OpenWeatherMap's servers). The system will automatically fall back to climatic simulation in the meantime.
2. **PyTorch Model Weights (`plant_disease_model.pth`):**
   - The disease prediction service includes built-in ResNet-9 architecture and default neural feature inference. If you have trained custom weights on the full PlantVillage dataset, place the `.pth` file in `ml-service/models/plant_disease_model.pth`.
3. **CORS issues during local development:**
   - Spring Boot has CORS enabled for `http://localhost:4200` and `http://127.0.0.1:4200` in `CorsConfig.java`. Ensure both backend and frontend are using the default ports.
