#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Trap SIGINT (Ctrl+C)
trap cleanup SIGINT

echo "Starting CareEnforced AI..."

# Start Backend
echo "Starting Backend (FastAPI)..."
cd backend
../.venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to initialize
sleep 2

# Start Frontend
echo "Starting Frontend (Vite)..."
cd ../frontend
npm run dev -- --host &
FRONTEND_PID=$!

echo "Application is running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop."

wait
