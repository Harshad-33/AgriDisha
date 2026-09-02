import { Component, ElementRef, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { TranslationService, LanguageOption } from '../../core/services/translation.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  isMenuCollapsed = true;
  isLangDropdownOpen = false;
  searchQuery = '';

  constructor(
    public authService: AuthService,
    public translationService: TranslationService,
    private router: Router,
    private elementRef: ElementRef
  ) {}

  toggleMenu(): void {
    this.isMenuCollapsed = !this.isMenuCollapsed;
  }

  toggleLangDropdown(event?: Event): void {
    if (event) {
      event.stopPropagation();
    }
    this.isLangDropdownOpen = !this.isLangDropdownOpen;
    if (this.isLangDropdownOpen) {
      this.searchQuery = '';
    }
  }

  closeLangDropdown(): void {
    this.isLangDropdownOpen = false;
  }

  selectLanguage(code: string): void {
    this.translationService.setLanguage(code);
    this.isLangDropdownOpen = false;
    this.isMenuCollapsed = true;
  }

  get filteredLanguages(): LanguageOption[] {
    const q = this.searchQuery.trim().toLowerCase();
    if (!q) {
      return this.translationService.languages;
    }
    return this.translationService.languages.filter(
      (l) => l.name.toLowerCase().includes(q) || l.nativeName.toLowerCase().includes(q) || l.code.toLowerCase().includes(q)
    );
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/home']);
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    if (!this.elementRef.nativeElement.contains(event.target)) {
      this.isLangDropdownOpen = false;
    }
  }
}
