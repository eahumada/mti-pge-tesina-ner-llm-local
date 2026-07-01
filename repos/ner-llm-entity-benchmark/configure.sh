#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "=================================================="
echo "🔧 Configuring project environment and dependencies"
echo "=================================================="

# Ensure setup.sh has execution permissions
chmod +x setup.sh

# Run the setup script to establish the virtual environment, install python libraries, and verify models
./setup.sh

echo "=================================================="
echo "✅ Project configured successfully!"
echo "=================================================="
