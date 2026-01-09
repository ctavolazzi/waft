import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import fs from 'fs';
import path from 'path';

const certPath = path.resolve(__dirname, 'localhost.pem');
const keyPath = path.resolve(__dirname, 'localhost-key.pem');

// Disable HTTPS for now - use HTTP on port 8781
let httpsConfig = false;
// if (fs.existsSync(certPath) && fs.existsSync(keyPath)) {
// 	httpsConfig = {
// 		cert: fs.readFileSync(certPath),
// 		key: fs.readFileSync(keyPath)
// 	};
// }

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		port: 8781,
		strictPort: true, // Force port 8781
		host: '0.0.0.0', // Listen on all interfaces
		https: false, // Use HTTP, not HTTPS
		proxy: {
			'/api': {
				target: 'http://localhost:8001',
				changeOrigin: true
			}
		}
	}
});
