import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api/generate-pdf': {
        target:
          'http://eaw47johq1lfkhf0hhh99e380plbbkaa.lambda-url.us-east-1.localhost.localstack.cloud:4566/',
        changeOrigin: true,
        secure: false,
        rewrite: () => '' // clear path
      }
    }
  }
})
