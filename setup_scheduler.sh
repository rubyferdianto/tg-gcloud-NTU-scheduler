#!/bin/bash

# Configuration
PROJECT_ID="PROJECT_ID"  # Update with your project ID
REGION="us-central1"
SERVICE_NAME="telegram-bot"
JOB_NAME="keep-warm-telegram-bot"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🕐 Setting up Cloud Scheduler to keep service warm${NC}"

# Enable Cloud Scheduler API
echo -e "${YELLOW}🔧 Enabling Cloud Scheduler API${NC}"
gcloud services enable cloudscheduler.googleapis.com

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

# Create or update the scheduler job
echo -e "${YELLOW}⏰ Creating scheduler job to ping service every 5 minutes${NC}"
gcloud scheduler jobs create http $JOB_NAME \
    --location=$REGION \
    --schedule="*/5 * * * *" \
    --uri="$SERVICE_URL/ping" \
    --http-method=GET \
    --description="Keep Telegram bot service warm" \
    --attempt-deadline=30s \
    --max-retry-attempts=3 \
    --max-retry-duration=120s \
    --min-backoff-duration=5s \
    --max-backoff-duration=300s || \
gcloud scheduler jobs update http $JOB_NAME \
    --location=$REGION \
    --schedule="*/5 * * * *" \
    --uri="$SERVICE_URL/ping" \
    --http-method=GET

echo -e "${GREEN}✅ Cloud Scheduler job created!${NC}"
echo -e "${YELLOW}📡 Service will be pinged every 5 minutes at: $SERVICE_URL/ping${NC}"
echo -e "${YELLOW}💡 This will keep your container warm and scheduler running${NC}"

# Test the ping endpoint
echo -e "${YELLOW}🧪 Testing ping endpoint${NC}"
curl -s "$SERVICE_URL/ping" | python3 -m json.tool

echo -e "${GREEN}🎉 Setup complete!${NC}"
