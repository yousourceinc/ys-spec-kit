#!/bin/bash
# Quick setup script for OAuth credentials

echo "🔐 Specify CLI - OAuth Setup"
echo "=============================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "⚠️  .env file already exists"
    read -p "Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Prompt for credentials
echo "Enter your GitHub OAuth credentials:"
echo ""

read -p "Client ID (Iv1.xxxxxxxxxxxxx): " CLIENT_ID
read -p "Client Secret: " -s CLIENT_SECRET
echo ""
read -p "Organization name: " ORG_NAME

# Validate inputs
if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ] || [ -z "$ORG_NAME" ]; then
    echo "❌ All fields are required"
    exit 1
fi

# Create .env file
cat > .env << EOF
# GitHub OAuth Configuration for Specify CLI
SPECIFY_GITHUB_CLIENT_ID=$CLIENT_ID
SPECIFY_GITHUB_CLIENT_SECRET=$CLIENT_SECRET
SPECIFY_GITHUB_ORG=$ORG_NAME
EOF

echo "✅ Created .env file"
echo ""

# Ask if they want to add to shell profile
echo "Add to shell profile for permanent setup?"
read -p "(y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    SHELL_RC="$HOME/.zshrc"
    
    if ! grep -q "SPECIFY_GITHUB_CLIENT_ID" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "# GitHub OAuth for Specify CLI" >> "$SHELL_RC"
        echo "export SPECIFY_GITHUB_CLIENT_ID=\"$CLIENT_ID\"" >> "$SHELL_RC"
        echo "export SPECIFY_GITHUB_CLIENT_SECRET=\"$CLIENT_SECRET\"" >> "$SHELL_RC"
        echo "export SPECIFY_GITHUB_ORG=\"$ORG_NAME\"" >> "$SHELL_RC"
        
        echo "✅ Added to $SHELL_RC"
        echo "Run: source $SHELL_RC"
    else
        echo "⚠️  Already exists in $SHELL_RC"
    fi
fi

echo ""
echo "Next steps:"
echo "  1. Load environment: export \$(cat .env | xargs)"
echo "  2. Test OAuth: node src/auth/github-oauth.js test"
echo "  3. Initialize project: node bin/specify.js init test-project"
echo ""
echo "Done! 🚀"
