package com.agridisha.controller;

import com.agridisha.dto.AuthRequest;
import com.agridisha.dto.AuthResponse;
import com.agridisha.dto.RegisterRequest;
import com.agridisha.dto.ResendOtpRequest;
import com.agridisha.dto.SendOtpRequest;
import com.agridisha.dto.VerifyOtpRegisterRequest;
import com.agridisha.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthService authService;

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "UP"));
    }

    /**
     * Step 1: Validate registration info and send 6-digit verification OTP.
     */
    @PostMapping("/send-otp")
    public ResponseEntity<Map<String, Object>> sendOtp(@Valid @RequestBody SendOtpRequest request) {
        Map<String, Object> response = authService.initiateRegistration(request);
        return ResponseEntity.ok(response);
    }

    /**
     * Resend verification OTP with 30-second cooldown protection.
     */
    @PostMapping("/resend-otp")
    public ResponseEntity<Map<String, Object>> resendOtp(@Valid @RequestBody ResendOtpRequest request) {
        Map<String, Object> response = authService.resendRegistrationOtp(request.getEmail());
        return ResponseEntity.ok(response);
    }

    /**
     * Step 2: Validate 6-digit OTP, persist user, and return JWT token for direct login.
     */
    @PostMapping("/verify-otp-register")
    public ResponseEntity<AuthResponse> verifyOtpAndRegister(@Valid @RequestBody VerifyOtpRegisterRequest request) {
        AuthResponse response = authService.verifyOtpAndCompleteRegistration(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Direct registration without OTP (legacy / direct API endpoint).
     */
    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@Valid @RequestBody RegisterRequest request) {
        AuthResponse response = authService.register(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Login endpoint with username or email.
     */
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody AuthRequest request) {
        AuthResponse response = authService.login(request);
        return ResponseEntity.ok(response);
    }
}
