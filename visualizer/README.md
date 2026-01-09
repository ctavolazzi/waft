# Waft Visualizer

SvelteKit-based development dashboard for Waft projects.

## Development

```bash
# Install dependencies
npm install

# Start dev server (runs on port 5173)
npm run dev

# The FastAPI backend should be running on port 8000
# Start it with: waft serve --dev
```

## Building

```bash
# Build for production
npm run build

# The build output will be in the `build/` directory
# The FastAPI server will serve these files when running `waft serve`
```

## Project Structure

- `src/routes/` - SvelteKit routes
- `src/lib/components/` - Reusable components
- `src/lib/stores/` - Svelte stores for state management
- `src/lib/api/` - API client for FastAPI backend
