#!/bin/bash
# Stop Recap and Review Docker services

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"

cd "$APP_DIR"

echo "🛑 Stopping Recap and Review Docker services..."

docker-compose down

echo "✅ Services stopped!"
