package com.agridisha.service;

import com.agridisha.dto.WeatherResponse;
import com.agridisha.exception.WeatherServiceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class WeatherService {

    private static final Logger logger = LoggerFactory.getLogger(WeatherService.class);

    @Value("${agridisha.weather.api-key:}")
    private String apiKey;

    @Value("${agridisha.weather.api-url:https://api.openweathermap.org/data/2.5/weather}")
    private String apiUrl;

    @Autowired
    private RestTemplate restTemplate;

    // Built-in climatic knowledge base for fallback
    private static final Map<String, double[]> CITY_CLIMATES = new HashMap<>();

    static {
        // [temperature, humidity]
        CITY_CLIMATES.put("mumbai", new double[]{28.5, 78.0});
        CITY_CLIMATES.put("delhi", new double[]{31.0, 55.0});
        CITY_CLIMATES.put("bangalore", new double[]{24.0, 68.0});
        CITY_CLIMATES.put("bengaluru", new double[]{24.0, 68.0});
        CITY_CLIMATES.put("kolkata", new double[]{29.5, 80.0});
        CITY_CLIMATES.put("chennai", new double[]{30.5, 82.0});
        CITY_CLIMATES.put("pune", new double[]{26.0, 62.0});
        CITY_CLIMATES.put("hyderabad", new double[]{28.0, 65.0});
        CITY_CLIMATES.put("ahmedabad", new double[]{32.0, 52.0});
        CITY_CLIMATES.put("jaipur", new double[]{30.0, 48.0});
        CITY_CLIMATES.put("lucknow", new double[]{29.0, 66.0});
        CITY_CLIMATES.put("patna", new double[]{28.5, 72.0});
        CITY_CLIMATES.put("chandigarh", new double[]{26.5, 58.0});
        CITY_CLIMATES.put("nagpur", new double[]{29.0, 60.0});
        CITY_CLIMATES.put("london", new double[]{16.0, 75.0});
        CITY_CLIMATES.put("new york", new double[]{18.5, 60.0});
        CITY_CLIMATES.put("tokyo", new double[]{20.0, 70.0});
        CITY_CLIMATES.put("sydney", new double[]{22.0, 65.0});
    }

    public WeatherResponse getWeatherForCity(String city) {
        if (!StringUtils.hasText(city)) {
            throw new WeatherServiceException("City name cannot be empty.");
        }

        String trimmedCity = city.trim();

        // If API key is configured, call OpenWeatherMap
        if (StringUtils.hasText(apiKey) && !"your_key".equalsIgnoreCase(apiKey) && !"test_key".equalsIgnoreCase(apiKey)) {
            try {
                String requestUrl = String.format("%s?q=%s&appid=%s&units=metric", apiUrl, trimmedCity, apiKey);
                ResponseEntity<Map> response = restTemplate.getForEntity(requestUrl, Map.class);

                if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                    Map<String, Object> body = response.getBody();
                    Map<String, Object> main = (Map<String, Object>) body.get("main");
                    List<Map<String, Object>> weatherList = (List<Map<String, Object>>) body.get("weather");

                    Double temp = main.get("temp") != null ? ((Number) main.get("temp")).doubleValue() : 25.0;
                    Double hum = main.get("humidity") != null ? ((Number) main.get("humidity")).doubleValue() : 65.0;

                    String desc = "Clear sky";
                    String icon = "01d";
                    if (weatherList != null && !weatherList.isEmpty()) {
                        desc = (String) weatherList.get(0).getOrDefault("description", "Clear sky");
                        icon = (String) weatherList.get(0).getOrDefault("icon", "01d");
                    }

                    String officialCityName = (String) body.getOrDefault("name", trimmedCity);
                    return new WeatherResponse(officialCityName, Math.round(temp * 10.0) / 10.0, hum, desc, icon, false);
                }
            } catch (Exception ex) {
                logger.warn("OpenWeatherMap API call failed for city '{}': {}. Falling back to simulation.", trimmedCity, ex.getMessage());
            }
        }

        // Fallback realistic climate simulator
        return getSimulatedWeather(trimmedCity);
    }

    private WeatherResponse getSimulatedWeather(String city) {
        String key = city.toLowerCase();
        double[] climate = CITY_CLIMATES.get(key);

        double temp;
        double hum;
        if (climate != null) {
            temp = climate[0];
            hum = climate[1];
        } else {
            // Deterministic hash based simulation for unlisted cities
            int hash = Math.abs(city.hashCode());
            temp = 20.0 + (hash % 160) / 10.0; // 20.0 to 36.0 C
            hum = 45.0 + (hash % 450) / 10.0;  // 45.0 to 90.0 %
        }

        return new WeatherResponse(
                city.substring(0, 1).toUpperCase() + city.substring(1),
                Math.round(temp * 10.0) / 10.0,
                Math.round(hum * 10.0) / 10.0,
                "Partly cloudy (Simulated)",
                "02d",
                true
        );
    }
}
