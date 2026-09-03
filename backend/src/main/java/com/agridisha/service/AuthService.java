package com.agridisha.service;

import com.agridisha.config.JwtTokenProvider;
import com.agridisha.dto.AuthRequest;
import com.agridisha.dto.AuthResponse;
import com.agridisha.dto.RegisterRequest;
import com.agridisha.dto.SendOtpRequest;
import com.agridisha.dto.VerifyOtpRegisterRequest;
import com.agridisha.entity.Role;
import com.agridisha.entity.User;
import com.agridisha.exception.BadRequestException;
import com.agridisha.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtTokenProvider tokenProvider;

    @Autowired
    private OtpService otpService;

    @Autowired
    private EmailService emailService;

    /**
     * Step 1: Validate uniqueness, generate 6-digit OTP, store registration session, dispatch email.
     */
    public java.util.Map<String, Object> initiateRegistration(SendOtpRequest request) {
        String username = request.getUsername().trim();
        String email = request.getEmail().trim().toLowerCase();

        if (userRepository.existsByUsername(username)) {
            throw new BadRequestException("Username '" + username + "' is already taken. Please choose another.");
        }
        if (userRepository.existsByEmail(email)) {
            throw new BadRequestException("Email '" + email + "' is already registered. Please sign in.");
        }

        String otp = otpService.storeOtp(request);
        boolean sentViaEmail = emailService.sendVerificationOtpEmail(email, request.getFullName(), otp);

        if (!sentViaEmail) {
            throw new BadRequestException("Unable to send verification OTP to '" + email + "'. Please check your email address and try again.");
        }

        java.util.Map<String, Object> response = new java.util.HashMap<>();
        response.put("email", email);
        response.put("smtpDelivered", true);
        response.put("message", "Verification code sent to " + email);
        return response;
    }

    /**
     * Resend verification OTP for pending registration.
     */
    public java.util.Map<String, Object> resendRegistrationOtp(String email) {
        String cleanEmail = email.trim().toLowerCase();
        if (userRepository.existsByEmail(cleanEmail)) {
            throw new BadRequestException("Email '" + cleanEmail + "' is already registered.");
        }

        String newOtp = otpService.resendOtp(cleanEmail);
        boolean sentViaEmail = emailService.sendVerificationOtpEmail(cleanEmail, "Farmer", newOtp);

        if (!sentViaEmail) {
            throw new BadRequestException("Unable to resend verification OTP to '" + cleanEmail + "'. Please try again.");
        }

        java.util.Map<String, Object> response = new java.util.HashMap<>();
        response.put("email", cleanEmail);
        response.put("smtpDelivered", true);
        response.put("message", "New verification code sent to " + cleanEmail);
        return response;
    }

    /**
     * Step 2: Verify 6-digit OTP, persist user in database, issue JWT token for direct login.
     */
    public AuthResponse verifyOtpAndCompleteRegistration(VerifyOtpRegisterRequest request) {
        String email = request.getEmail().trim().toLowerCase();
        OtpService.PendingRegistration pending = otpService.validateAndConsumeOtp(email, request.getOtp());

        if (userRepository.existsByUsername(pending.getUsername())) {
            throw new BadRequestException("Username '" + pending.getUsername() + "' is already taken.");
        }
        if (userRepository.existsByEmail(pending.getEmail())) {
            throw new BadRequestException("Email '" + pending.getEmail() + "' is already registered.");
        }

        User user = new User();
        user.setUsername(pending.getUsername());
        user.setEmail(pending.getEmail());
        user.setPassword(passwordEncoder.encode(pending.getPassword()));
        user.setFullName(pending.getFullName() != null && !pending.getFullName().isBlank() ? pending.getFullName() : pending.getUsername());
        user.setLocation(pending.getLocation() != null && !pending.getLocation().isBlank() ? pending.getLocation() : "Maharashtra, India");
        user.setRole(Role.ROLE_USER);

        User savedUser = userRepository.save(user);
        String token = tokenProvider.generateToken(savedUser.getUsername());

        return new AuthResponse(
                token,
                savedUser.getId(),
                savedUser.getUsername(),
                savedUser.getEmail(),
                savedUser.getFullName(),
                savedUser.getRole().name()
        );
    }

    /**
     * Direct registration without OTP (retained for backward compatibility).
     */
    public AuthResponse register(RegisterRequest request) {
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new BadRequestException("Username '" + request.getUsername() + "' is already taken.");
        }
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new BadRequestException("Email '" + request.getEmail() + "' is already registered.");
        }

        User user = new User();
        user.setUsername(request.getUsername().trim());
        user.setEmail(request.getEmail().trim().toLowerCase());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setFullName(request.getFullName() != null ? request.getFullName().trim() : request.getUsername());
        user.setLocation(request.getLocation() != null ? request.getLocation().trim() : "Unknown");
        user.setRole(Role.ROLE_USER);

        User savedUser = userRepository.save(user);
        String token = tokenProvider.generateToken(savedUser.getUsername());

        return new AuthResponse(
                token,
                savedUser.getId(),
                savedUser.getUsername(),
                savedUser.getEmail(),
                savedUser.getFullName(),
                savedUser.getRole().name()
        );
    }

    public AuthResponse login(AuthRequest request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getUsername().trim(), request.getPassword())
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);
        String token = tokenProvider.generateToken(request.getUsername().trim());

        User user = userRepository.findByUsername(request.getUsername().trim())
                .or(() -> userRepository.findByEmail(request.getUsername().trim()))
                .orElseThrow(() -> new BadRequestException("User record not found."));

        return new AuthResponse(
                token,
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                user.getFullName(),
                user.getRole().name()
        );
    }

    public Optional<User> getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated() || "anonymousUser".equals(authentication.getPrincipal())) {
            return Optional.empty();
        }
        String username = authentication.getName();
        return userRepository.findByUsername(username).or(() -> userRepository.findByEmail(username));
    }
}
