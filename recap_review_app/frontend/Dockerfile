# Modern Electron Docker Container
# Based on rpi-electron architecture but updated for 2024-2025 best practices
# Uses Xvfb for headless display instead of X11 forwarding

# Stage 1: Builder
FROM node:20-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy application source
COPY . .

# Stage 2: Runtime
FROM node:20-slim

# Install Electron runtime dependencies and Xvfb
RUN apt-get update && apt-get install -y \
    # Electron dependencies
    libgtk-3-0 \
    libnotify4 \
    libnss3 \
    libxss1 \
    libasound2 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    # Xvfb for headless display
    xvfb \
    # Fonts for PDF rendering
    fonts-liberation \
    fonts-dejavu-core \
    # Utilities
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r electron && useradd -r -g electron -u 1000 electron \
    && mkdir -p /home/electron && chown -R electron:electron /home/electron

WORKDIR /app

# Copy built application from builder
COPY --from=builder --chown=electron:electron /app /app

# Set display for Xvfb
ENV DISPLAY=:99

# Switch to non-root user
USER electron

# Expose port for VNC (optional)
EXPOSE 5900

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f "electron" > /dev/null || exit 1

# Start Xvfb and Electron app
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 & sleep 2 && npm start"]
