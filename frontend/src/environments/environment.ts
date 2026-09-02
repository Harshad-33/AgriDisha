// Environment configuration with dynamic backend resolution
// Connects to local backend when running on localhost, and to live Render cloud backend on Vercel/production.

export const environment = {
  production: true,
  apiUrl: (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'))
    ? 'http://localhost:8080/api'
    : 'https://agridisha-backend.onrender.com/api'
};
