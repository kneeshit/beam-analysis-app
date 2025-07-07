# Installation Guide

## Quick Start

### Option 1: Automated Setup (Windows)
1. Double-click `setup_and_run.bat` to install all dependencies
2. Run `start_backend.bat` in one terminal
3. Run `start_frontend.bat` in another terminal
4. Open `http://localhost:3000` in your browser

### Option 2: Manual Setup

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python run.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Detailed Installation Steps

### Prerequisites
- **Python 3.8+**: Download from [python.org](https://python.org)
- **Node.js 16+**: Download from [nodejs.org](https://nodejs.org)
- **Git** (optional): For cloning the repository

### Step 1: Backend Installation

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Test backend installation**:
   ```bash
   python run.py
   ```
   You should see: "Uvicorn running on http://0.0.0.0:8000"

### Step 2: Frontend Installation

1. **Open a new terminal** and navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```
   Your browser should automatically open to `http://localhost:3000`

## Verification

### Backend Verification
- Visit `http://localhost:8000` - should show: `{"message": "Beam Analysis API is running"}`
- Visit `http://localhost:8000/docs` - should show FastAPI documentation

### Frontend Verification
- Visit `http://localhost:3000` - should show the Beam Analysis application
- Check browser console for any errors

## Troubleshooting

### Common Issues

#### Python Issues
- **"python not found"**: Install Python and add to PATH
- **"pip not found"**: Reinstall Python with pip option checked
- **Permission errors**: Use virtual environment or run as administrator

#### Node.js Issues
- **"npm not found"**: Install Node.js and restart terminal
- **"EACCES permission denied"**: Use `npm config set prefix ~/.npm-global`
- **Port 3000 in use**: Kill process using port or change port in package.json

#### Network Issues
- **CORS errors**: Ensure backend is running on port 8000
- **API connection failed**: Check if backend server is accessible
- **Firewall blocking**: Allow Python and Node.js through firewall

### Port Configuration

#### Backend Port (default: 8000)
Change in `backend/run.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
```

#### Frontend Port (default: 3000)
Set environment variable:
```bash
set PORT=3001 && npm start  # Windows
PORT=3001 npm start         # macOS/Linux
```

### Dependencies

#### Backend Dependencies
- fastapi==0.104.1
- uvicorn==0.24.0
- pydantic==2.5.0
- numpy==1.24.3
- matplotlib==3.7.2
- Pillow==10.0.1

#### Frontend Dependencies
- react==18.2.0
- @mui/material==5.14.0
- axios==1.6.0

## Development Setup

### Backend Development
```bash
cd backend
pip install -r requirements.txt
python run.py  # Runs with auto-reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start  # Runs with hot reload
```

### API Testing
Use the FastAPI docs at `http://localhost:8000/docs` to test API endpoints directly.

## Production Deployment

### Backend Production
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Production
```bash
npm run build
# Serve the build folder with a web server
```

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Verify all prerequisites are installed
3. Check terminal/console for error messages
4. Ensure both servers are running on correct ports
