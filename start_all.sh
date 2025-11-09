#!/bin/bash

# RailAnnounce - Start All Services Script
# This script helps you start all services needed for RailAnnounce

echo "🚂 RailAnnounce - Starting All Services"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Error: manage.py not found. Please run this script from the Django_project directory.${NC}"
    exit 1
fi

echo -e "${YELLOW}This script will help you start all services.${NC}"
echo -e "${YELLOW}You need to run each service in a separate terminal.${NC}"
echo ""

# Check if migrations are done
if [ ! -f "db.sqlite3" ] && [ ! -d "announcements/migrations/0001_initial.py" ]; then
    echo -e "${YELLOW}Running migrations first...${NC}"
    python3 manage.py makemigrations
    python3 manage.py migrate
    echo -e "${GREEN}✓ Migrations completed${NC}"
    echo ""
fi

echo "========================================"
echo "STEP 1: Start LibreTranslate Server"
echo "========================================"
echo ""
echo "Run this command in Terminal 1:"
echo -e "${GREEN}docker run -ti --rm -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en${NC}"
echo ""
echo "OR if Docker is not available:"
echo -e "${GREEN}# cd LibreTranslate && python main.py --host 127.0.0.1 --port 5000${NC}"
echo ""
read -p "Press Enter when LibreTranslate is running..."

echo ""
echo "========================================"
echo "STEP 2: Start Redis Server"
echo "========================================"
echo ""
echo "Run this command in Terminal 2:"
echo -e "${GREEN}redis-server${NC}"
echo ""
read -p "Press Enter when Redis is running..."

echo ""
echo "========================================"
echo "STEP 3: Start Celery Worker"
echo "========================================"
echo ""
echo "Run this command in Terminal 3:"
echo -e "${GREEN}cd $(pwd) && celery -A railannounce worker --loglevel=info${NC}"
echo ""
read -p "Press Enter when Celery worker is running..."

echo ""
echo "========================================"
echo "STEP 4: Start Django Server"
echo "========================================"
echo ""
echo "Run this command in Terminal 4:"
echo -e "${GREEN}cd $(pwd) && python3 manage.py runserver${NC}"
echo ""
read -p "Press Enter to start Django server now..."

echo ""
echo -e "${GREEN}Starting Django server...${NC}"
echo ""
python3 manage.py runserver


