#!/bin/bash
# CausalityCare Full Stack Deployment Script

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== CausalityCare Deployment Script ===${NC}"

# Step 1: Get the Railway API URL
read -p "Enter your Railway API URL (e.g., https://causalitycare-prod-abc.up.railway.app): " RAILWAY_URL

if [ -z "$RAILWAY_URL" ]; then
  echo "❌ Railway URL cannot be empty!"
  exit 1
fi

echo -e "${GREEN}✓ Using Railway API: $RAILWAY_URL${NC}"

# Step 2: Update frontend API endpoint
echo -e "${BLUE}Updating frontend API endpoint...${NC}"

FRONTEND_SERVICE="/Users/shrinikatelu/causalitycare/frontend/src/app/services/causality.service.ts"

# Read the file and update the apiUrl
sed -i '' "s|private apiUrl = 'http://localhost:8000'|private apiUrl = '$RAILWAY_URL'|g" "$FRONTEND_SERVICE"

echo -e "${GREEN}✓ Frontend API endpoint updated${NC}"

# Step 3: Build frontend
echo -e "${BLUE}Building frontend for production...${NC}"

cd /Users/shrinikatelu/causalitycare/frontend

ng build --configuration production --base-href "/causalitycare/"

echo -e "${GREEN}✓ Frontend built successfully${NC}"

# Step 4: Deploy to GitHub Pages
echo -e "${BLUE}Deploying to GitHub Pages...${NC}"

npx angular-cli-ghpages --dir=dist/causalitycare

echo -e "${GREEN}✓ Deployed to GitHub Pages!${NC}"

# Step 5: Display results
echo -e "${BLUE}=== Deployment Complete ===${NC}"
echo -e "${GREEN}✓ Frontend: https://ShrinikaTelu.github.io/causalitycare/${NC}"
echo -e "${GREEN}✓ Backend: $RAILWAY_URL${NC}"
echo ""
echo "Verify your deployment works by visiting:"
echo "  https://ShrinikaTelu.github.io/causalitycare/"
