import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Router, NavigationEnd } from '@angular/router';

export interface LanguageOption {
  code: string;
  name: string;
  nativeName: string;
  isPopular?: boolean;
}

declare global {
  interface Window {
    google: any;
    googleTranslateElementInit: any;
  }
}

@Injectable({
  providedIn: 'root'
})
export class TranslationService {
  private readonly STORAGE_KEY = 'agridisha_lang';

  // 22 Official Scheduled Languages of India + English
  public readonly languages: LanguageOption[] = [
    { code: 'en', name: 'English', nativeName: 'English', isPopular: true },
    { code: 'mr', name: 'Marathi', nativeName: 'मराठी', isPopular: true },
    { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी', isPopular: true },
    { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી', isPopular: true },
    { code: 'bn', name: 'Bengali', nativeName: 'বাংলা', isPopular: true },
    { code: 'te', name: 'Telugu', nativeName: 'తెలుగు', isPopular: true },
    { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்', isPopular: true },
    { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ', isPopular: true },
    { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ' },
    { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം' },
    { code: 'or', name: 'Odia', nativeName: 'ଓଡ଼ିଆ' },
    { code: 'as', name: 'Assamese', nativeName: 'অসমীয়া' },
    { code: 'ur', name: 'Urdu', nativeName: 'اردو' },
    { code: 'kok', name: 'Konkani', nativeName: 'कोंकणी' },
    { code: 'mai', name: 'Maithili', nativeName: 'मैथिली' },
    { code: 'sa', name: 'Sanskrit', nativeName: 'संस्कृतम्' },
    { code: 'ne', name: 'Nepali', nativeName: 'नेपाली' },
    { code: 'sd', name: 'Sindhi', nativeName: 'سنڌي / सिंधी' },
    { code: 'doi', name: 'Dogri', nativeName: 'डोगरी' },
    { code: 'mni-Mtei', name: 'Manipuri', nativeName: 'মৈতৈলোন্' },
    { code: 'brx', name: 'Bodo', nativeName: 'बर\'' },
    { code: 'sat', name: 'Santali', nativeName: 'ᱥᱟᱱᱛᱟᱲᱤ' },
    { code: 'ks', name: 'Kashmiri', nativeName: 'کٲشُر' }
  ];

  private currentLangSubject = new BehaviorSubject<LanguageOption>(this.languages[0]);
  public currentLang$ = this.currentLangSubject.asObservable();

  constructor(private router: Router) {
    this.initLanguage();

    // Reapply translation after Angular route navigation
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        const lang = this.currentLangSubject.value;
        if (lang.code !== 'en') {
          setTimeout(() => this.triggerGoogleTranslate(lang.code), 300);
        }
      }
    });
  }

  private initLanguage(): void {
    const savedCode = localStorage.getItem(this.STORAGE_KEY) || 'en';
    const found = this.languages.find((l) => l.code === savedCode) || this.languages[0];
    this.currentLangSubject.next(found);

    if (savedCode !== 'en') {
      // Set googtrans cookie on boot
      this.setGoogleTransCookie(savedCode);
    }
  }

  public setLanguage(code: string): void {
    const selected = this.languages.find((l) => l.code === code) || this.languages[0];
    this.currentLangSubject.next(selected);
    localStorage.setItem(this.STORAGE_KEY, selected.code);

    if (selected.code === 'en') {
      this.resetToEnglish();
    } else {
      this.setGoogleTransCookie(selected.code);
      this.triggerGoogleTranslate(selected.code);
    }
  }

  public get currentLanguage(): LanguageOption {
    return this.currentLangSubject.value;
  }

  private setGoogleTransCookie(code: string): void {
    const domain = window.location.hostname;
    const cookieVal = code === 'en' ? '' : `/en/${code}`;
    const expires = code === 'en' ? 'expires=Thu, 01 Jan 1970 00:00:00 UTC;' : 'expires=Fri, 31 Dec 9999 23:59:59 GMT;';

    document.cookie = `googtrans=${cookieVal}; ${expires} path=/;`;
    document.cookie = `googtrans=${cookieVal}; ${expires} path=/; domain=${domain};`;
    document.cookie = `googtrans=${cookieVal}; ${expires} path=/; domain=.${domain};`;

    if (code !== 'en') {
      document.cookie = `googtrans=/auto/${code}; ${expires} path=/;`;
      document.cookie = `googtrans=/auto/${code}; ${expires} path=/; domain=${domain};`;
      document.cookie = `googtrans=/auto/${code}; ${expires} path=/; domain=.${domain};`;
    }
  }

  private resetToEnglish(): void {
    const domain = window.location.hostname;
    document.cookie = `googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    document.cookie = `googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${domain};`;
    document.cookie = `googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.${domain};`;

    const selectEl = document.querySelector('.goog-te-combo') as HTMLSelectElement;
    if (selectEl) {
      selectEl.value = '';
      selectEl.dispatchEvent(new Event('change', { bubbles: true }));
    }
    setTimeout(() => {
      window.location.reload();
    }, 150);
  }

  private triggerGoogleTranslate(langCode: string): void {
    const applyToSelect = (el: HTMLSelectElement): boolean => {
      if (el) {
        el.value = langCode;
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.dispatchEvent(new Event('input', { bubbles: true }));
        return true;
      }
      return false;
    };

    const selectEl = document.querySelector('.goog-te-combo') as HTMLSelectElement;
    if (applyToSelect(selectEl)) {
      return;
    }

    // If widget combo is not yet in DOM, poll briefly, then fallback to reload
    let attempts = 0;
    const interval = setInterval(() => {
      attempts++;
      const el = document.querySelector('.goog-te-combo') as HTMLSelectElement;
      if (applyToSelect(el)) {
        clearInterval(interval);
      } else if (attempts > 12) {
        clearInterval(interval);
        // Reload ensures the googtrans cookie translates everything on startup
        window.location.reload();
      }
    }, 200);
  }
}
