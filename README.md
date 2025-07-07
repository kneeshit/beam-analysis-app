# Structural Beam Analysis Web Application

A full-stack web application for structural beam analysis, converted from a Streamlit application to React.js frontend with FastAPI backend. This application performs comprehensive structural engineering calculations including shear force, bending moment, slope, and deflection analysis for beams with various load configurations.

## Features

### Frontend (React.js)
- **Interactive Beam Configuration**: Set beam length, support locations, and material properties
- **Load Input System**: Add four types of loads:
  - Point Moments
  - Point Forces  
  - Constant Force Profiles
  - Triangular Force Profiles
- **Real-time Beam Visualization**: Dynamic beam schematic with loads and supports
- **Engineering Diagrams**: Interactive plots for shear force, bending moment, slope, and deflection
- **Load Management**: View, add, and clear loads with real-time updates
- **Responsive Design**: Works on desktop and mobile devices

### Backend (FastAPI)
- **RESTful API**: Clean API endpoints for all operations
- **Session Management**: Multi-user support with session-based state
- **Mathematical Engine**: Accurate structural analysis calculations
- **Image Generation**: Dynamic beam schematics and engineering plots
- **Error Handling**: Comprehensive validation and error responses

## Project Structure

```
beam-analysis-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application and routes
│   │   ├── models.py            # Pydantic data models
│   │   ├── calculations.py      # Structural analysis functions
│   │   ├── visualization.py     # Image generation (PIL + matplotlib)
│   │   └── session_manager.py   # Session state management
│   ├── requirements.txt         # Python dependencies
│   └── run.py                   # Application runner
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── BeamInput.js
│   │   │   ├── LoadInput.js
│   │   │   ├── BeamVisualization.js
│   │   │   ├── LoadList.js
│   │   │   └── ResultsDisplay.js
│   │   ├── services/
│   │   │   └── api.js           # API service layer
│   │   ├── App.js               # Main application component
│   │   ├── App.css              # Styling
│   │   └── index.js             # React entry point
│   └── package.json             # Node.js dependencies
└── README.md
```

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python run.py
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend application will be available at `http://localhost:3000`

## Usage

1. **Start both servers**: Ensure both backend (port 8000) and frontend (port 3000) are running
2. **Open the application**: Navigate to `http://localhost:3000` in your browser
3. **Configure beam properties**: Set beam length, support locations, and material properties
4. **Add loads**: Use the load input tabs to add different types of loads to your beam
5. **Visualize**: See real-time updates to the beam schematic as you add loads
6. **Analyze**: Click "Calculate Analysis" to perform structural analysis
7. **Review results**: View engineering diagrams and maximum values

## API Endpoints

### Session Management
- `POST /api/session/create` - Create a new session
- `DELETE /api/session/{session_id}` - Delete a session

### Beam Configuration
- `POST /api/session/{session_id}/beam-properties` - Set beam properties

### Load Management
- `POST /api/session/{session_id}/loads/add` - Add a load
- `GET /api/session/{session_id}/loads` - Get all loads
- `DELETE /api/session/{session_id}/loads/clear` - Clear all loads

### Analysis and Visualization
- `POST /api/session/{session_id}/calculate` - Perform structural analysis
- `GET /api/session/{session_id}/beam-image` - Get beam schematic image
- `GET /api/session/{session_id}/plot/{plot_type}` - Get engineering diagrams

## Technical Details

### Mathematical Engine
The application uses numerical integration and structural analysis principles to calculate:
- **Shear Force**: Distribution along the beam length
- **Bending Moment**: Moment distribution with support reactions
- **Slope**: Angular deflection using moment-area method
- **Deflection**: Vertical displacement with boundary conditions

### Load Types Supported
1. **Point Moments**: Concentrated moments at specific locations
2. **Point Forces**: Concentrated forces at specific locations
3. **Constant Force Profiles**: Uniformly distributed loads over a range
4. **Triangular Force Profiles**: Linearly varying distributed loads

### Session Management
Each user session maintains:
- Beam properties (length, supports, material properties)
- All applied loads
- Calculation state and results

## Development

### Adding New Features
1. **Backend**: Add new endpoints in `main.py`, models in `models.py`, calculations in `calculations.py`
2. **Frontend**: Create new components in `components/`, update API calls in `services/api.js`

### Testing
- Backend: Use FastAPI's automatic documentation at `http://localhost:8000/docs`
- Frontend: Use React Developer Tools for component debugging

## Troubleshooting

### Common Issues
1. **CORS Errors**: Ensure backend CORS settings allow frontend origin
2. **Port Conflicts**: Change ports in configuration if 3000/8000 are in use
3. **Dependencies**: Ensure all requirements are installed correctly
4. **Session Errors**: Refresh the page to create a new session

### Performance
- Sessions are stored in memory - restart backend to clear all sessions
- Large numbers of calculation points may slow down analysis
- Image generation is optimized but may take time for complex beams

## License

This project is for educational and professional use in structural engineering applications.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions, please check the troubleshooting section or create an issue in the repository.
