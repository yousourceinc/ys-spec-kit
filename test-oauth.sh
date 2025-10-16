#!/bin/bash
# Quick script to load .env and test OAuth

set -e

cd "$(dirname "$0")" || exit 1

echo "📦 Loading environment variables from .env..."
export $(cat .env | xargs)

echo "✓ Environment variables loaded"
echo "  Client ID: $SPECIFY_GITHUB_CLIENT_ID"
echo "  Organization: $SPECIFY_GITHUB_ORG"
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not found"
    echo "Install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo ""
echo "🔐 Testing OAuth authentication..."
echo "(This will open your browser for GitHub authorization)"
echo ""

node src/auth/github-oauth.js test
