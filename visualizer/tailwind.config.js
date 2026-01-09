/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				primary: {
					DEFAULT: '#7c9eff',
					dark: '#6b8eff',
					light: '#8dafff'
				},
				bg: {
					dark: '#0a0e1a',
					card: '#1a1e29',
					'card-hover': '#232834'
				},
				text: {
					primary: '#e8eaf6',
					secondary: '#b0b8d0',
					muted: '#707890'
				},
				success: '#4ade80',
				warning: '#fbbf24',
				error: '#f87171',
				info: '#60a5fa'
			}
		}
	},
	plugins: []
};
