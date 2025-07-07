import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert
} from '@mui/material';
import api from '../services/api';

const BeamVisualization = ({ beamProperties, loads, refreshTrigger }) => {
  const [beamImage, setBeamImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBeamImage = async () => {
      if (!beamProperties || !api.sessionId) return;
      
      setLoading(true);
      setError('');
      
      try {
        const imageData = await api.getBeamImage();
        setBeamImage(imageData);
      } catch (err) {
        setError('Failed to load beam visualization');
        console.error('Error fetching beam image:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchBeamImage();
  }, [beamProperties, loads, refreshTrigger]);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Beam Visualization
        </Typography>
        
        <Box 
          sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            minHeight: 400,
            border: '1px solid #e0e0e0',
            borderRadius: 1,
            backgroundColor: '#fafafa'
          }}
        >
          {loading && <CircularProgress />}
          
          {error && (
            <Alert severity="error" sx={{ width: '100%' }}>
              {error}
            </Alert>
          )}
          
          {beamImage && !loading && !error && (
            <img 
              src={beamImage} 
              alt="Beam Schematic" 
              style={{ 
                maxWidth: '100%', 
                maxHeight: '400px',
                objectFit: 'contain'
              }}
            />
          )}
          
          {!beamImage && !loading && !error && (
            <Typography color="textSecondary">
              Beam visualization will appear here
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};

export default BeamVisualization;
