import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // The browser only talks to Vite; Vite forwards /api/* to FastAPI. Same origin, so no CORS needed.
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
