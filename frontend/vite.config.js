import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [vue()],
    build: {
        outDir: '../static/dist',
        emptyOutDir: true
    },
    server: {
        host: '0.0.0.0',
        port: 5173,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true
            },
            '/upload': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true
            },
            '/login': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true
            },
            '/logout': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true
            },
            '/query': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true
            }
        }
    }
})
