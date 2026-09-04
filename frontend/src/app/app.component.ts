import { Component, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { FooterComponent } from './shared/footer/footer.component';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, FooterComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'AgriDisha';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // Silent pre-warming ping to wake up cloud backend immediately so all subsequent user actions are instant
    this.http.get(`${environment.apiUrl}/auth/health`).subscribe({
      next: () => {},
      error: () => {}
    });
  }
}
