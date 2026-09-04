import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit, OnDestroy {
  step: 'DETAILS' | 'OTP' = 'DETAILS';
  registerForm: FormGroup;
  otpForm: FormGroup;

  isLoading = false;
  errorMessage = '';
  successMessage = '';
  resendCountdown = 0;
  private timerInterval: any = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.registerForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      fullName: ['', [Validators.required]],
      location: ['', [Validators.required]]
    });

    this.otpForm = this.fb.group({
      otp: ['', [Validators.required, Validators.pattern('^[0-9]{6}$')]]
    });
  }

  ngOnInit(): void {
    // Pre-warm backend while user is filling out registration details
    this.authService.pingHealth().subscribe({
      next: () => {},
      error: () => {}
    });
  }

  get userEmail(): string {
    return this.registerForm.get('email')?.value || '';
  }

  // Step 1: Submit Details and Request OTP
  onSubmitDetails(): void {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.authService.sendOtp(this.registerForm.value).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.step = 'OTP';
        this.successMessage = res.message || `Verification code sent to ${this.userEmail}`;
        this.startResendTimer(60);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.error?.message || 'Failed to send verification code. Please check your details.';
      }
    });
  }

  // Step 2: Verify 6-digit OTP and complete direct registration
  onVerifyOtp(): void {
    if (this.otpForm.invalid) {
      this.otpForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const payload = {
      email: this.userEmail,
      otp: this.otpForm.get('otp')?.value.trim()
    };

    this.authService.verifyOtpAndRegister(payload).subscribe({
      next: () => {
        this.isLoading = false;
        this.clearIntervalTimer();
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.error?.message || 'Invalid or expired verification code. Please try again.';
      }
    });
  }

  // Resend OTP
  onResendOtp(): void {
    if (this.resendCountdown > 0 || this.isLoading) return;

    this.isLoading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.authService.resendOtp(this.userEmail).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.successMessage = res.message || 'A new verification code has been dispatched.';
        this.startResendTimer(60);
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMessage = err.error?.message || 'Failed to resend code. Please wait a moment.';
      }
    });
  }

  // Return to Step 1 to edit email or credentials
  onBackToDetails(): void {
    this.step = 'DETAILS';
    this.errorMessage = '';
    this.successMessage = '';
    this.otpForm.reset();
    this.clearIntervalTimer();
  }

  private startResendTimer(seconds: number): void {
    this.clearIntervalTimer();
    this.resendCountdown = seconds;
    this.timerInterval = setInterval(() => {
      this.resendCountdown--;
      if (this.resendCountdown <= 0) {
        this.clearIntervalTimer();
      }
    }, 1000);
  }

  private clearIntervalTimer(): void {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  ngOnDestroy(): void {
    this.clearIntervalTimer();
  }
}
