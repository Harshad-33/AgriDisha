package com.agridisha.service;

import jakarta.mail.internet.MimeMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@Service
public class EmailService {

    private static final Logger logger = LoggerFactory.getLogger(EmailService.class);

    @Autowired(required = false)
    private JavaMailSender mailSender;

    @Autowired
    private RestTemplate restTemplate;

    @Value("${spring.mail.username:}")
    private String senderEmail;

    @Value("${BREVO_API_KEY:${agridisha.mail.brevo-api-key:}}")
    private String brevoApiKey;

    /**
     * Send 6-digit OTP verification email with HTML styling.
     * Supports:
     * 1. Brevo HTTP API (Port 443 HTTPS - guaranteed to work in cloud environments like Render that block SMTP port 587)
     * 2. Spring JavaMailSender SMTP (Port 587 - works locally and in unblocked environments)
     */
    public boolean sendVerificationOtpEmail(String recipientEmail, String recipientName, String otp) {
        String subject = "AgriDisha - Your Email Verification Code: " + otp;
        String htmlContent = buildOtpHtmlTemplate(recipientName, otp);

        // 1. First priority in cloud: If Brevo HTTP API key is configured, send via HTTPS Port 443
        if (brevoApiKey != null && !brevoApiKey.isBlank()) {
            try {
                HttpHeaders headers = new HttpHeaders();
                headers.setContentType(MediaType.APPLICATION_JSON);
                headers.set("api-key", brevoApiKey.trim());

                String fromEmail = (senderEmail != null && !senderEmail.isBlank()) ? senderEmail.trim() : "harshadporajwar21@gmail.com";
                Map<String, Object> sender = Map.of("name", "AgriDisha Smart Agriculture", "email", fromEmail);
                Map<String, Object> recipient = Map.of("email", recipientEmail, "name", recipientName != null ? recipientName : "Farmer");

                Map<String, Object> body = Map.of(
                        "sender", sender,
                        "to", List.of(recipient),
                        "subject", subject,
                        "htmlContent", htmlContent
                );

                HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);
                ResponseEntity<String> response = restTemplate.postForEntity("https://api.brevo.com/v3/smtp/email", entity, String.class);

                if (response.getStatusCode().is2xxSuccessful()) {
                    logger.info("Successfully dispatched verification OTP to {} via Brevo HTTPS API (Port 443)", recipientEmail);
                    return true;
                }
            } catch (Exception ex) {
                logger.error("Brevo HTTPS mail delivery failed: {}", ex.getMessage());
            }
        }

        // 2. Second priority: Standard JavaMailSender SMTP (Gmail port 587)
        if (mailSender != null && senderEmail != null && !senderEmail.isBlank()) {
            try {
                MimeMessage message = mailSender.createMimeMessage();
                MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

                helper.setFrom(senderEmail, "AgriDisha Smart Agriculture");
                helper.setTo(recipientEmail);
                helper.setSubject(subject);
                helper.setText(htmlContent, true);

                mailSender.send(message);
                logger.info("Successfully dispatched verification OTP email to {} via SMTP", recipientEmail);
                return true;
            } catch (Exception e) {
                logger.warn("SMTP mail delivery failed (host may block outbound SMTP port 587): {}", e.getMessage());
            }
        }

        logger.error("No active email channel succeeded for recipient: {}", recipientEmail);
        return false;
    }

    private String buildOtpHtmlTemplate(String name, String otp) {
        String displayName = (name != null && !name.isBlank()) ? name : "Farmer";
        return "<!DOCTYPE html>" +
                "<html>" +
                "<head><meta charset='UTF-8'></head>" +
                "<body style='margin:0; padding:20px; background-color:#f4f6f8; font-family:Arial, sans-serif;'>" +
                "  <table align='center' width='100%' max-width='600' style='max-width:600px; background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 15px rgba(0,0,0,0.08);'>" +
                "    <tr>" +
                "      <td style='background:#107c41; padding:30px; text-align:center; color:#ffffff;'>" +
                "        <h1 style='margin:0; font-size:26px; font-weight:800; letter-spacing:1px;'>🌱 AgriDisha</h1>" +
                "        <p style='margin:6px 0 0 0; font-size:14px; opacity:0.9;'>Smart Agriculture Recommendation System</p>" +
                "      </td>" +
                "    </tr>" +
                "    <tr>" +
                "      <td style='padding:35px 30px; color:#2d3748;'>" +
                "        <h2 style='margin:0 0 16px 0; font-size:20px; color:#1a202c;'>Email Verification Code</h2>" +
                "        <p style='font-size:15px; line-height:1.6; color:#4a5568;'>Hello <b>" + displayName + "</b>,</p>" +
                "        <p style='font-size:15px; line-height:1.6; color:#4a5568;'>Thank you for registering with <b>AgriDisha</b>. To complete your account registration and secure your farm profile, please enter the one-time verification code below:</p>" +
                "        <div style='text-align:center; margin:30px 0;'>" +
                "          <span style='display:inline-block; background:#e8f5e9; border:2px dashed #107c41; color:#107c41; font-size:32px; font-weight:bold; letter-spacing:8px; padding:15px 30px; border-radius:8px; font-family:monospace;'>" + otp + "</span>" +
                "        </div>" +
                "        <p style='font-size:14px; color:#718096; line-height:1.5; margin-bottom:20px;'>⏱️ This code is valid for <b>10 minutes</b>. For security reasons, do not share this code with anyone.</p>" +
                "        <hr style='border:none; border-top:1px solid #edf2f7; margin:25px 0;'>" +
                "        <p style='font-size:13px; color:#a0aec0; margin:0;'>If you did not initiate this registration, please ignore this email.</p>" +
                "      </td>" +
                "    </tr>" +
                "    <tr>" +
                "      <td style='background:#f7fafc; padding:20px; text-align:center; font-size:12px; color:#a0aec0; border-top:1px solid #edf2f7;'>" +
                "        © " + java.time.Year.now().getValue() + " AgriDisha Platform. Empowering Modern Precision Agriculture." +
                "      </td>" +
                "    </tr>" +
                "  </table>" +
                "</body>" +
                "</html>";
    }
}
