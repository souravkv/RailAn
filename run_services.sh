#!/bin/bash

# RailAnnounce - Run All Services in Separate Terminals
# This script opens 4 terminals, one for each service

echo "🚂 RailAnnounce - Starting All Services in Separate Terminals"
echo "=============================================================="
echo ""

# Get the project directory
PROJECT_DIR="/home/zourv/Documents/PROJEX/Django_project"
cd "$PROJECT_DIR" || exit

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found. Please check PROJECT_DIR in this script."
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
if ! command_exists gnome-terminal && ! command_exists xterm && ! command_exists konsole; then
    echo "Error: No terminal emulator found (gnome-terminal, xterm, or konsole)"
    echo "Please run services manually in separate terminals (see START_HERE.md)"
    exit 1
fi

echo "Opening 4 terminals for:"
echo "1. LibreTranslate Server"
echo "2. Redis Server"
echo "3. Celery Worker"
echo "4. Django Server"
echo ""

# Determine which terminal to use
if command_exists gnome-terminal; then
    TERMINAL="gnome-terminal"
    TERMINAL_OPTS="--tab"
elif command_exists xterm; then
    TERMINAL="xterm"
    TERMINAL_OPTS="-e"
elif command_exists konsole; then
    TERMINAL="konsole"
    TERMINAL_OPTS="--new-tab"
fi

# Run migrations first if needed
if [ ! -f "db.sqlite3" ]; then
    echo "Running migrations..."
    python3 manage.py makemigrations >/dev/null 2>&1
    python3 manage.py migrate >/dev/null 2>&1
    echo "✓ Migrations completed"
    echo ""
fi

# Terminal 1: LibreTranslate (Docker)
if command_exists docker; then
    echo "Opening Terminal 1: LibreTranslate (Docker)..."
    $TERMINAL $TERMINAL_OPTS bash -c "echo 'LibreTranslate Server - Terminal 1'; echo ''; docker run -ti --rm -p 5000:5000 libretranslate/libretranslate --load-only hi,ta,te,bn,kn,en; exec bash" &
    sleep 2
else
    echo "Docker not found. Please start LibreTranslate manually in Terminal 1"
    echo "See START_HERE.md for instructions"
fi

# Terminal 2: Redis
if command_exists redis-server; then
    echo "Opening Terminal 2: Redis Server..."
    $TERMINAL $TERMINAL_OPTS bash -c "echo 'Redis Server - Terminal 2'; echo ''; redis-server; exec bash" &
    sleep 2
else
    echo "Redis not found. Please install: sudo apt-get install redis-server"
fi

# Terminal 3: Celery Worker
echo "Opening Terminal 3: Celery Worker..."
$TERMINAL $TERMINAL_OPTS bash -c "cd '$PROJECT_DIR' && echo 'Celery Worker - Terminal 3'; echo ''; celery -A railannounce worker --loglevel=info; exec bash" &
sleep 2

# Terminal 4: Django Server
echo "Opening Terminal 4: Django Server..."
$TERMINAL $TERMINAL_OPTS bash -c "cd '$PROJECT_DIR' && echo 'Django Server - Terminal 4'; echo ''; python3 manage.py runserver; exec bash" &
sleep 2

echo ""
echo "=============================================================="
echo "✓ All services started in separate terminals!"
echo "=============================================================="
echo ""
echo "Wait a few seconds for services to start, then:"
echo "  - LibreTranslate: http://127.0.0.1:5000"
echo "  - Django App: http://127.0.0.1:8000"
echo ""
echo "To stop services, press Ctrl+C in each terminal"
echo ""


