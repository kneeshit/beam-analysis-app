import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Box,
  Tabs,
  Tab,
  Slider,
  Alert,
  Divider
} from '@mui/material';

const LoadInput = ({ beamProperties, onAddLoad }) => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [error, setError] = useState('');
  
  // Load input states
  const [pointMoment, setPointMoment] = useState({ magnitude: 0, location: beamProperties.length / 2 });
  const [pointForce, setPointForce] = useState({ magnitude: 0, location: beamProperties.length / 2 });
  const [constantProfile, setConstantProfile] = useState({ 
    magnitude: 0, 
    start_location: beamProperties.length / 4, 
    end_location: (3 * beamProperties.length) / 4 
  });
  const [triangularProfile, setTriangularProfile] = useState({ 
    magnitude: 0, 
    start_location: beamProperties.length / 4, 
    end_location: (3 * beamProperties.length) / 4 
  });

  const loadTypes = [
    'Point Moment',
    'Point Force', 
    'Constant Force Profile',
    'Triangular Force Profile'
  ];

  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue);
    setError('');
  };

  const handleAddLoad = async () => {
    setError('');
    
    try {
      let loadType, loadData;
      
      switch (selectedTab) {
        case 0:
          loadType = 'Point Moment';
          loadData = pointMoment;
          break;
        case 1:
          loadType = 'Point Force';
          loadData = pointForce;
          break;
        case 2:
          loadType = 'Constant Force Profile';
          loadData = constantProfile;
          break;
        case 3:
          loadType = 'Triangular Force Profile';
          loadData = triangularProfile;
          break;
        default:
          return;
      }
      
      await onAddLoad(loadType, loadData);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error adding load');
    }
  };

  const renderPointMomentInput = () => (
    <Box>
      <TextField
        label="Point Moment Magnitude (N-m)"
        type="number"
        value={pointMoment.magnitude}
        onChange={(e) => setPointMoment({ ...pointMoment, magnitude: parseFloat(e.target.value) || 0 })}
        fullWidth
        margin="normal"
        inputProps={{ step: 0.01 }}
      />
      <Typography gutterBottom sx={{ mt: 2 }}>
        Point Moment Location: {pointMoment.location} m
      </Typography>
      <Slider
        value={pointMoment.location}
        onChange={(e, value) => setPointMoment({ ...pointMoment, location: value })}
        min={0}
        max={beamProperties.length}
        step={0.1}
        marks
        valueLabelDisplay="auto"
      />
    </Box>
  );

  const renderPointForceInput = () => (
    <Box>
      <TextField
        label="Point Force Magnitude (N)"
        type="number"
        value={pointForce.magnitude}
        onChange={(e) => setPointForce({ ...pointForce, magnitude: parseFloat(e.target.value) || 0 })}
        fullWidth
        margin="normal"
        inputProps={{ step: 0.01 }}
      />
      <Typography gutterBottom sx={{ mt: 2 }}>
        Point Force Location: {pointForce.location} m
      </Typography>
      <Slider
        value={pointForce.location}
        onChange={(e, value) => setPointForce({ ...pointForce, location: value })}
        min={0}
        max={beamProperties.length}
        step={0.1}
        marks
        valueLabelDisplay="auto"
      />
    </Box>
  );

  const renderConstantProfileInput = () => (
    <Box>
      <TextField
        label="'w' Magnitude (N/m)"
        type="number"
        value={constantProfile.magnitude}
        onChange={(e) => setConstantProfile({ ...constantProfile, magnitude: parseFloat(e.target.value) || 0 })}
        fullWidth
        margin="normal"
        inputProps={{ step: 0.01 }}
      />
      <Typography gutterBottom sx={{ mt: 2 }}>
        Constant Force Profile Range: {constantProfile.start_location} m to {constantProfile.end_location} m
      </Typography>
      <Slider
        value={[constantProfile.start_location, constantProfile.end_location]}
        onChange={(e, value) => setConstantProfile({ 
          ...constantProfile, 
          start_location: value[0], 
          end_location: value[1] 
        })}
        min={0}
        max={beamProperties.length}
        step={0.1}
        marks
        valueLabelDisplay="auto"
      />
    </Box>
  );

  const renderTriangularProfileInput = () => (
    <Box>
      <TextField
        label="'w₀' Magnitude (N)"
        type="number"
        value={triangularProfile.magnitude}
        onChange={(e) => setTriangularProfile({ ...triangularProfile, magnitude: parseFloat(e.target.value) || 0 })}
        fullWidth
        margin="normal"
        inputProps={{ step: 0.01 }}
      />
      <Typography gutterBottom sx={{ mt: 2 }}>
        Triangular Force Profile Range: {triangularProfile.start_location} m to {triangularProfile.end_location} m
      </Typography>
      <Slider
        value={[triangularProfile.start_location, triangularProfile.end_location]}
        onChange={(e, value) => setTriangularProfile({ 
          ...triangularProfile, 
          start_location: value[0], 
          end_location: value[1] 
        })}
        min={0}
        max={beamProperties.length}
        step={0.1}
        marks
        valueLabelDisplay="auto"
      />
    </Box>
  );

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Load Input
        </Typography>
        
        <Tabs value={selectedTab} onChange={handleTabChange} variant="scrollable" scrollButtons="auto">
          {loadTypes.map((type, index) => (
            <Tab key={index} label={type} />
          ))}
        </Tabs>

        <Box sx={{ mt: 2 }}>
          {selectedTab === 0 && renderPointMomentInput()}
          {selectedTab === 1 && renderPointForceInput()}
          {selectedTab === 2 && renderConstantProfileInput()}
          {selectedTab === 3 && renderTriangularProfileInput()}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        <Divider sx={{ my: 2 }} />

        <Button 
          variant="contained" 
          onClick={handleAddLoad}
          fullWidth
          sx={{ mt: 2 }}
        >
          Add Load
        </Button>
      </CardContent>
    </Card>
  );
};

export default LoadInput;
