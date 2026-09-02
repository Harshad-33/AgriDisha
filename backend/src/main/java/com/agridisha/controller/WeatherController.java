package com.agridisha.controller;

import com.agridisha.dto.WeatherResponse;
import com.agridisha.service.WeatherService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/weather")
public class WeatherController {

    @Autowired
    private WeatherService weatherService;

    @GetMapping("/{city}")
    public ResponseEntity<WeatherResponse> getWeather(@PathVariable String city) {
        WeatherResponse response = weatherService.getWeatherForCity(city);
        return ResponseEntity.ok(response);
    }
}
