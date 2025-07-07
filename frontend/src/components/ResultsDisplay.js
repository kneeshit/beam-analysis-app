import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Grid,
  CircularProgress,
  Alert,
  Divider,
  Paper
} from '@mui/material';
import api from '../services/api';

const ResultsDisplay = ({ beamProperties, loads }) => {
  const [results, setResults] = useState(null);
  const [plots, setPlots] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCalculate = async () => {
    setLoading(true);
    setError('');
    setResults(null);
    setPlots({});

    try {
      // Calculate analysis
      const analysisResults = await api.calculateAnalysis();
      setResults(analysisResults);

      // Generate all plots
      const plotTypes = ['shear', 'moment', 'slope', 'deflection'];
      const plotPromises = plotTypes.map(async (type) => {
        try {
          const plotImage = await api.getEngineeringPlot(type);
          return { type, image: plotImage };
        } catch (err) {
          console.error(`Error generating ${type} plot:`, err);
          return { type, error: err.message };
        }
      });

      const plotResults = await Promise.all(plotPromises);
      const plotsData = {};
      plotResults.forEach(({ type, image, error }) => {
        if (image) {
          plotsData[type] = image;
        } else if (error) {
          plotsData[type] = { error };
        }
      });
      
      setPlots(plotsData);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error performing analysis');
    } finally {
      setLoading(false);
    }
  };

  const renderPlot = (plotType, title, maxValue, unit) => (
    <Grid item xs={12} md={6} key={plotType}>
      <Paper elevation={2} sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        
        <Box 
          sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            minHeight: 300,
            border: '1px solid #e0e0e0',
            borderRadius: 1,
            backgroundColor: '#fafafa',
            mb: 2
          }}
        >
          {plots[plotType] && !plots[plotType].error ? (
            <img 
              src={plots[plotType]} 
              alt={title}
              style={{ 
                maxWidth: '100%', 
                maxHeight: '300px',
                objectFit: 'contain'
              }}
            />
          ) : plots[plotType]?.error ? (
            <Alert severity="error">
              Failed to generate {title.toLowerCase()}
            </Alert>
          ) : (
            <Typography color="textSecondary">
              {title} will appear here after calculation
            </Typography>
          )}
        </Box>
        
        {maxValue !== undefined && (
          <Typography variant="body2" color="textSecondary">
            Maximum {title.split(' ')[0]}: {maxValue.toFixed(6)} {unit}
          </Typography>
        )}
      </Paper>
    </Grid>
  );

  const totalLoads = Object.values(loads).reduce((sum, loadArray) => sum + loadArray.length, 0);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Analysis Results
        </Typography>

        <Button 
          variant="contained" 
          onClick={handleCalculate}
          disabled={loading || totalLoads === 0}
          fullWidth
          sx={{ mb: 3 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Calculate Analysis'}
        </Button>

        {totalLoads === 0 && (
          <Alert severity="info" sx={{ mb: 2 }}>
            Add loads to the beam to perform analysis
          </Alert>
        )}

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {results && (
          <Box>
            <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
              Summary
            </Typography>
            
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={6} sm={3}>
                <Paper elevation={1} sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="textSecondary">
                    Max Shear Force
                  </Typography>
                  <Typography variant="h6">
                    {results.max_shear_force.toFixed(3)} N
                  </Typography>
                </Paper>
              </Grid>
              
              <Grid item xs={6} sm={3}>
                <Paper elevation={1} sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="textSecondary">
                    Max Bending Moment
                  </Typography>
                  <Typography variant="h6">
                    {results.max_bending_moment.toFixed(3)} N⋅m
                  </Typography>
                </Paper>
              </Grid>
              
              <Grid item xs={6} sm={3}>
                <Paper elevation={1} sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="textSecondary">
                    Max Deflection
                  </Typography>
                  <Typography variant="h6">
                    {results.max_deflection.toFixed(6)} m
                  </Typography>
                </Paper>
              </Grid>
              
              <Grid item xs={6} sm={3}>
                <Paper elevation={1} sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="textSecondary">
                    Max Slope
                  </Typography>
                  <Typography variant="h6">
                    {results.max_slope.toFixed(6)} rad
                  </Typography>
                </Paper>
              </Grid>
            </Grid>

            <Divider sx={{ my: 3 }} />

            <Typography variant="h6" gutterBottom>
              Engineering Diagrams
            </Typography>
            
            <Grid container spacing={3}>
              {renderPlot('shear', 'Shear Force Diagram', results.max_shear_force, 'N')}
              {renderPlot('moment', 'Bending Moment Diagram', results.max_bending_moment, 'N⋅m')}
              {renderPlot('deflection', 'Deflection Diagram', results.max_deflection, 'm')}
              {renderPlot('slope', 'Slope Diagram', results.max_slope, 'rad')}
            </Grid>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ResultsDisplay;
