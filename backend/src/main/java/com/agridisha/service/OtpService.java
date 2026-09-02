package com.agridisha.service;

import com.agridisha.dto.SendOtpRequest;
import com.agridisha.exception.BadRequestException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.security.SecureRandom;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class OtpService {

    private static final Logger logger = LoggerFactory.getLogger(OtpService.class);
    private static final long OTP_VALIDITY_DURATION_MS = 10 * 60 * 1000; // 10 minutes
    private static final long RESEND_COOLDOWN_MS = 30 * 1000; // 30 seconds
    private static final int MAX_VERIFICATION_ATTEMPTS = 5;

    private final SecureRandom secureRandom = new SecureRandom();
    private final Map<String, PendingRegistration> pendingRegistrations = new ConcurrentHashMap<>();

    public static class PendingRegistration {
        private final String username;
        private final String email;
        private final String password;
        private final String fullName;
        private final String location;
        private String otp;
        private long expiryTime;
        private long lastSentTime;
        private int attempts;

        public PendingRegistration(String username, String email, String password, String fullName, String location, String otp, long expiryTime, long lastSentTime) {
            this.username = username;
            this.email = email;
            this.password = password;
            this.fullName = fullName;
            this.location = location;
            this.otp = otp;
            this.expiryTime = expiryTime;
            this.lastSentTime = lastSentTime;
            this.attempts = 0;
        }

        public String getUsername() { return username; }
        public String getEmail() { return email; }
        public String getPassword() { return password; }
        public String getFullName() { return fullName; }
        public String getLocation() { return location; }
        public String getOtp() { return otp; }
        public void setOtp(String otp) { this.otp = otp; }
        public long getExpiryTime() { return expiryTime; }
        public void setExpiryTime(long expiryTime) { this.expiryTime = expiryTime; }
        public long getLastSentTime() { return lastSentTime; }
        public void setLastSentTime(long lastSentTime) { this.lastSentTime = lastSentTime; }
        public int getAttempts() { return attempts; }
        public void incrementAttempts() { this.attempts++; }
    }

    /**
     * Generate 6-digit numeric OTP.
     */
    public String generateOtp() {
        int code = 100000 + secureRandom.nextInt(900000);
        return String.valueOf(code);
    }

    /**
     * Store registration data and generated OTP in thread-safe memory.
     */
    public String storeOtp(SendOtpRequest request) {
        String emailKey = request.getEmail().toLowerCase().trim();
        String otp = generateOtp();
        long now = System.currentTimeMillis();

        PendingRegistration pending = new PendingRegistration(
                request.getUsername().trim(),
                emailKey,
                request.getPassword(),
                request.getFullName().trim(),
                request.getLocation().trim(),
                otp,
                now + OTP_VALIDITY_DURATION_MS,
                now
        );

        pendingRegistrations.put(emailKey, pending);
        logger.info("Generated 6-digit OTP [{}] for email: {}", otp, emailKey);
        return otp;
    }

    /**
     * Resend OTP for an existing pending registration with cooldown enforcement.
     */
    public String resendOtp(String email) {
        String emailKey = email.toLowerCase().trim();
        PendingRegistration pending = pendingRegistrations.get(emailKey);

        if (pending == null) {
            throw new BadRequestException("No pending registration found for this email. Please restart registration.");
        }

        long now = System.currentTimeMillis();
        if (now - pending.getLastSentTime() < RESEND_COOLDOWN_MS) {
            long remainingSeconds = (RESEND_COOLDOWN_MS - (now - pending.getLastSentTime())) / 1000;
            throw new BadRequestException("Please wait " + remainingSeconds + " seconds before requesting a new code.");
        }

        String newOtp = generateOtp();
        pending.setOtp(newOtp);
        pending.setExpiryTime(now + OTP_VALIDITY_DURATION_MS);
        pending.setLastSentTime(now);

        logger.info("Resent newly generated 6-digit OTP [{}] for email: {}", newOtp, emailKey);
        return newOtp;
    }

    /**
     * Validate OTP and return validated registration details.
     */
    public PendingRegistration validateAndConsumeOtp(String email, String inputOtp) {
        String emailKey = email.toLowerCase().trim();
        PendingRegistration pending = pendingRegistrations.get(emailKey);

        if (pending == null) {
            throw new BadRequestException("Verification session expired or not found. Please request a new code.");
        }

        long now = System.currentTimeMillis();
        if (now > pending.getExpiryTime()) {
            pendingRegistrations.remove(emailKey);
            throw new BadRequestException("Verification code has expired. Please request a new one.");
        }

        if (pending.getAttempts() >= MAX_VERIFICATION_ATTEMPTS) {
            pendingRegistrations.remove(emailKey);
            throw new BadRequestException("Maximum verification attempts exceeded. Please restart registration.");
        }

        if (!pending.getOtp().equals(inputOtp.trim())) {
            pending.incrementAttempts();
            int remaining = MAX_VERIFICATION_ATTEMPTS - pending.getAttempts();
            throw new BadRequestException("Invalid verification code. " + remaining + " attempts remaining.");
        }

        // Successfully verified: remove from pending cache
        pendingRegistrations.remove(emailKey);
        return pending;
    }
}
