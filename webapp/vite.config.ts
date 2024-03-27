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
          'http://giq89hp4l7a58hn6tlm4g9t5rt3t268z.lambda-url.us-east-1.localhost.localstack.cloud:4566/',
        changeOrigin: true,
        secure: false,
        rewrite: () => '' // clear path
      }
    }
  }
})
