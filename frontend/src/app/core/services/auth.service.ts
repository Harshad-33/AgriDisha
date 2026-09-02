import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { AuthResponse, User } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8080/api/auth';
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadUserFromStorage();
  }

  private loadUserFromStorage(): void {
    const token = localStorage.getItem('agridisha_token');
    const userJson = localStorage.getItem('agridisha_user');
    if (token && userJson) {
      try {
        const user: User = JSON.parse(userJson);
        this.currentUserSubject.next(user);
      } catch (e) {
        this.logout();
      }
    }
  }

  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  public get isAuthenticated(): boolean {
    return !!this.getToken();
  }

  public getToken(): string | null {
    return localStorage.getItem('agridisha_token');
  }

  sendOtp(data: any): Observable<{ message: string; email: string; otpPreview?: string; smtpDelivered?: boolean }> {
    return this.http.post<{ message: string; email: string; otpPreview?: string; smtpDelivered?: boolean }>(`${this.apiUrl}/send-otp`, data);
  }

  resendOtp(email: string): Observable<{ message: string; email: string; otpPreview?: string; smtpDelivered?: boolean }> {
    return this.http.post<{ message: string; email: string; otpPreview?: string; smtpDelivered?: boolean }>(`${this.apiUrl}/resend-otp`, { email });
  }

  verifyOtpAndRegister(data: { email: string; otp: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/verify-otp-register`, data).pipe(
      tap((res) => this.handleAuthSuccess(res))
    );
  }

  register(data: any): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/register`, data).pipe(
      tap((res) => this.handleAuthSuccess(res))
    );
  }

  login(data: any): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, data).pipe(
      tap((res) => this.handleAuthSuccess(res))
    );
  }

  private handleAuthSuccess(res: AuthResponse): void {
    if (res && res.token) {
      localStorage.setItem('agridisha_token', res.token);
      const user: User = {
        id: res.id,
        username: res.username,
        email: res.email,
        fullName: res.fullName,
        location: '',
        role: res.role
      };
      localStorage.setItem('agridisha_user', JSON.stringify(user));
      this.currentUserSubject.next(user);
    }
  }

  logout(): void {
    localStorage.removeItem('agridisha_token');
    localStorage.removeItem('agridisha_user');
    this.currentUserSubject.next(null);
  }
}
