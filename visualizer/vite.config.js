import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import fs from 'fs';
import path from 'path';

const certPath = path.resolve(__dirname, 'localhost.pem');
const keyPath = path.resolve(__dirname, 'localhost-key.pem');

let httpsConfig = false;
if (fs.existsSync(certPath) && fs.existsSync(keyPath)) {
	httpsConfig = {
		cert: fs.readFileSync(certPath),
		key: fs.readFileSync(keyPath)
	};
}

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		port: 5173,
		strictPort: false,
		host: true,
		https: httpsConfig,
		proxy: {
			'/api': {
				target: 'http://localhost:8000',
				changeOrigin: true
			}
		}
	}
});
