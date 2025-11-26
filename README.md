# CareEnforced AI

## How to Run

### Prerequisites
- Python 3.9+
- Node.js 18+

### Quick Start
1.  Open a terminal in this directory.
2.  Make the start script executable (first time only):
    ```bash
    chmod +x start_app.sh
    ```
3.  Run the app:
    ```bash
    ./start_app.sh
    ```
4.  Open your browser to [http://localhost:5173](http://localhost:5173).

### Manual Start
If you prefer to run components separately:

**Backend**:
```bash
cd backend
../.venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm run dev -- --host
```

## Mobile Demo
To demo on your phone, ensure your computer and phone are on the same Wi-Fi network.
See [Mobile Demo Tutorial](mobile_demo_tutorial.md) for detailed instructions.
