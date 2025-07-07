import React, { useState, useEffect } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Container,
  Grid,
  Alert,
  Snackbar,
  CircularProgress,
  Box,
  Typography
} from '@mui/material';
import './App.css';

import BeamInput from './components/BeamInput';
import LoadInput from './components/LoadInput';
import BeamVisualization from './components/BeamVisualization';
import LoadList from './components/LoadList';
import ResultsDisplay from './components/ResultsDisplay';
import api from './services/api';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [beamProperties, setBeamProperties] = useState({
    length: 50,
    support1: 12.5,
    support2: 37.5,
    modulus_of_elasticity: 1.0,
    second_moment_of_area: 1.0
  });
  
  const [loads, setLoads] = useState({
    point_moments: [],
    point_forces: [],
    constant_force_profiles: [],
    triangular_force_profiles: []
  });
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  // Initialize session on app start
  useEffect(() => {
    const initializeSession = async () => {
      try {
        await api.createSession();
        await api.setBeamProperties(beamProperties);
        setLoading(false);
      } catch (err) {
        setError('Failed to initialize application');
        setLoading(false);
      }
    };

    initializeSession();
  }, []);

  // Update beam properties when they change
  useEffect(() => {
    const updateBeamProperties = async () => {
      if (!api.sessionId) return;
      
      try {
        await api.setBeamProperties(beamProperties);
        setRefreshTrigger(prev => prev + 1);
      } catch (err) {
        setError('Failed to update beam properties');
      }
    };

    updateBeamProperties();
  }, [beamProperties]);

  // Load current loads from backend
  const refreshLoads = async () => {
    try {
      const currentLoads = await api.getLoads();
      setLoads(currentLoads);
      setRefreshTrigger(prev => prev + 1);
    } catch (err) {
      setError('Failed to refresh loads');
    }
  };

  const handleBeamPropertiesChange = (newProperties) => {
    setBeamProperties(newProperties);
  };

  const handleSupportLocationsChange = (newLocations) => {
    // This is handled in BeamInput component
  };

  const handleAddLoad = async (loadType, loadData) => {
    try {
      await api.addLoad(loadType, loadData);
      await refreshLoads();
      setSuccess('Load added successfully');
    } catch (err) {
      throw err; // Re-throw to be handled by LoadInput component
    }
  };

  const handleClearLoads = async () => {
    try {
      await api.clearLoads();
      await refreshLoads();
      setSuccess('All loads cleared');
    } catch (err) {
      setError('Failed to clear loads');
    }
  };

  const handleCloseSnackbar = () => {
    setError('');
    setSuccess('');
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box 
          sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100vh' 
          }}
        >
          <CircularProgress size={60} />
        </Box>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Structural Beam Analysis</h1>
          <p className="App-subtitle">Interactive Engineering Analysis Tool</p>
        </header>

        <Container maxWidth="xl" className="main-container">
          <Grid container spacing={3}>
            {/* Left Column - Main Controls and Results */}
            <Grid item xs={12} lg={8}>
              <div className="left-column">
                <BeamInput
                  beamProperties={beamProperties}
                  onBeamPropertiesChange={handleBeamPropertiesChange}
                  onSupportLocationsChange={handleSupportLocationsChange}
                />
                
                <LoadInput
                  beamProperties={beamProperties}
                  onAddLoad={handleAddLoad}
                />
                
                <ResultsDisplay
                  beamProperties={beamProperties}
                  loads={loads}
                />
              </div>
            </Grid>

            {/* Right Column - Visualization and Load List */}
            <Grid item xs={12} lg={4}>
              <div className="right-column">
                <BeamVisualization
                  beamProperties={beamProperties}
                  loads={loads}
                  refreshTrigger={refreshTrigger}
                />
                
                <LoadList
                  loads={loads}
                  onClearLoads={handleClearLoads}
                />
              </div>
            </Grid>
          </Grid>
        </Container>

        {/* Snackbar for notifications */}
        <Snackbar
          open={!!error}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert onClose={handleCloseSnackbar} severity="error" sx={{ width: '100%' }}>
            {error}
          </Alert>
        </Snackbar>

        <Snackbar
          open={!!success}
          autoHideDuration={3000}
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert onClose={handleCloseSnackbar} severity="success" sx={{ width: '100%' }}>
            {success}
          </Alert>
        </Snackbar>
      </div>
    </ThemeProvider>
  );
}

export default App;
