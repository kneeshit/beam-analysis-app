# Troubleshooting Guide

## Backend Issues

### Issue: "You must pass the application as an import string to enable 'reload' or 'workers'"

**Solution**: Use the updated startup script:
```bash
cd backend
python start_server.py
```

### Issue: Backend not responding / Connection refused

**Check these steps**:

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start backend server**:
   ```bash
   cd backend
   python start_server.py
   ```

3. **Verify backend is running**:
   - Open browser to `http://127.0.0.1:8000`
   - Should show: `{"message": "Beam Analysis API is running"}`

4. **Test backend functionality**:
   ```bash
   python test_backend.py
   ```

### Issue: Import errors or module not found

**Solution**: Make sure you're in the correct directory and dependencies are installed:
```bash
cd backend
pip install fastapi uvicorn pydantic numpy matplotlib pillow
python start_server.py
```

## Frontend Issues

### Issue: Frontend can't connect to backend

**Check these steps**:

1. **Ensure backend is running first**:
   ```bash
   cd backend
   python start_server.py
   ```

2. **Start frontend**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Check browser console** for error messages

### Issue: CORS errors

**Solution**: The backend is configured to allow frontend connections. If you still get CORS errors:

1. Make sure backend is running on port 8000
2. Make sure frontend is running on port 3000
3. Try accessing frontend via `http://localhost:3000` (not 127.0.0.1)

### Issue: "Network Error" or API calls failing

**Check**:
1. Backend server is running and accessible at `http://127.0.0.1:8000`
2. No firewall blocking the connection
3. Check browser developer tools Network tab for failed requests

## Step-by-Step Startup Process

### 1. Install Dependencies

**Backend**:
```bash
cd backend
pip install -r requirements.txt
```

**Frontend**:
```bash
cd frontend
npm install
```

### 2. Start Backend Server

```bash
cd backend
python start_server.py
```

**Expected output**:
```
Starting Beam Analysis Backend Server...
Server will be available at: http://localhost:8000
API documentation at: http://localhost:8000/docs
Press Ctrl+C to stop the server
--------------------------------------------------
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3. Test Backend (Optional)

```bash
python test_backend.py
```

### 4. Start Frontend

**In a new terminal**:
```bash
cd frontend
npm start
```

**Expected output**:
```
Compiled successfully!

You can now view beam-analysis-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

### 5. Open Application

Open browser to `http://localhost:3000`

## Common Error Messages

### Backend Errors

**"ModuleNotFoundError: No module named 'fastapi'"**
```bash
cd backend
pip install -r requirements.txt
```

**"Address already in use"**
- Another process is using port 8000
- Kill the process or change the port in `start_server.py`

**"Permission denied"**
- Run terminal as administrator (Windows)
- Use `sudo` (macOS/Linux)

### Frontend Errors

**"npm: command not found"**
- Install Node.js from [nodejs.org](https://nodejs.org)

**"Port 3000 is already in use"**
- Kill the process using port 3000
- Or set a different port: `PORT=3001 npm start`

**"Failed to compile"**
- Check for syntax errors in the console
- Make sure all dependencies are installed: `npm install`

## Testing Individual Components

### Test Backend API

Visit `http://127.0.0.1:8000/docs` for interactive API documentation

### Test Frontend Components

1. Open browser developer tools
2. Check Console tab for JavaScript errors
3. Check Network tab for failed API requests

## Port Configuration

### Change Backend Port

Edit `backend/start_server.py`:
```python
uvicorn.run(
    "app.main:app",
    host="127.0.0.1",
    port=8001,  # Change this
    reload=True,
    log_level="info"
)
```

Also update `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8001/api';
```

### Change Frontend Port

```bash
set PORT=3001 && npm start  # Windows
PORT=3001 npm start         # macOS/Linux
```

## Still Having Issues?

1. **Check all prerequisites are installed**:
   - Python 3.8+
   - Node.js 16+
   - All dependencies

2. **Try the automated setup**:
   ```bash
   # Windows
   setup_and_run.bat
   
   # Then run servers separately
   start_backend.bat
   start_frontend.bat
   ```

3. **Check firewall settings**:
   - Allow Python and Node.js through firewall
   - Allow ports 3000 and 8000

4. **Restart everything**:
   - Close all terminals
   - Restart both backend and frontend
   - Clear browser cache

5. **Check system resources**:
   - Ensure sufficient RAM and CPU
   - Close other applications if needed
