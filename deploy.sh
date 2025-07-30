#!/bin/bash

# Configuration - Update these values
PROJECT_ID="main-duality-467406-h5"
SERVICE_NAME="telegram-bot"
REGION="us-central1"
TELEGRAM_BOT_TOKEN="8300049409:AAGhYomw0vvPDwabom3jbj7pq2oSVjRNqoE"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Deploying Telegram Bot to Google Cloud Run${NC}"

# Check if required variables are set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo -e "${RED}❌ Please update PROJECT_ID in this script${NC}"
    exit 1
fi

if [ "$TELEGRAM_BOT_TOKEN" = "your-telegram-bot-token" ]; then
    echo -e "${RED}❌ Please update TELEGRAM_BOT_TOKEN in this script${NC}"
    exit 1
fi

# Set the project
echo -e "${YELLOW}📋 Setting project to $PROJECT_ID${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${YELLOW}🔧 Enabling required APIs${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Create secret for Telegram bot token (skip if already exists)
echo -e "${YELLOW}🔐 Creating secret for Telegram bot token${NC}"
if gcloud secrets describe telegram-bot-token >/dev/null 2>&1; then
    echo "Secret telegram-bot-token already exists, skipping creation"
else
    echo -n "$TELEGRAM_BOT_TOKEN" | gcloud secrets create telegram-bot-token --data-file=-
fi

# Build and deploy the container
echo -e "${YELLOW}🏗️  Building and deploying container${NC}"
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${YELLOW}📡 Service URL: $SERVICE_URL${NC}"

# Set the webhook URL environment variable and redeploy
echo -e "${YELLOW}🔗 Setting webhook URL and redeploying${NC}"
gcloud run services update $SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --set-env-vars "WEBHOOK_URL=$SERVICE_URL,TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN"

echo -e "${GREEN}✅ Webhook URL configured!${NC}"

# Set the webhook
echo -e "${YELLOW}📡 Setting webhook with Telegram${NC}"
curl -X POST "$SERVICE_URL/set_webhook"

echo -e "${GREEN}🎉 All done! Your Telegram bot is now running on Cloud Run${NC}"
echo -e "${YELLOW}💡 Test your bot by sending /start to it on Telegram${NC}"
