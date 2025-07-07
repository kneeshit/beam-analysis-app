import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Slider,
  Box,
  Divider
} from '@mui/material';

const BeamInput = ({ 
  beamProperties, 
  onBeamPropertiesChange, 
  onSupportLocationsChange 
}) => {
  const handlePropertyChange = (property, value) => {
    onBeamPropertiesChange({
      ...beamProperties,
      [property]: value
    });
  };

  const handleSupportChange = (event, newValue) => {
    onSupportLocationsChange(newValue);
    onBeamPropertiesChange({
      ...beamProperties,
      support1: newValue[0],
      support2: newValue[1]
    });
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Beam Properties
        </Typography>
        
        <Box sx={{ mb: 3 }}>
          <TextField
            label="Modulus of Elasticity 'E' (Pa)"
            type="number"
            value={beamProperties.modulus_of_elasticity}
            onChange={(e) => handlePropertyChange('modulus_of_elasticity', parseFloat(e.target.value) || 1)}
            fullWidth
            margin="normal"
            inputProps={{ step: 0.00001, min: 0.00001 }}
          />
        </Box>

        <Box sx={{ mb: 3 }}>
          <TextField
            label="Second Moment of Area 'I' (m⁴)"
            type="number"
            value={beamProperties.second_moment_of_area}
            onChange={(e) => handlePropertyChange('second_moment_of_area', parseFloat(e.target.value) || 1)}
            fullWidth
            margin="normal"
            inputProps={{ step: 0.01, min: 0.01 }}
          />
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom>
            Beam Length: {beamProperties.length} m
          </Typography>
          <Slider
            value={beamProperties.length}
            onChange={(e, value) => handlePropertyChange('length', value)}
            min={1}
            max={100}
            step={1}
            marks
            valueLabelDisplay="auto"
          />
        </Box>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom>
            Support Locations: {beamProperties.support1} m and {beamProperties.support2} m
          </Typography>
          <Slider
            value={[beamProperties.support1, beamProperties.support2]}
            onChange={handleSupportChange}
            min={0}
            max={beamProperties.length}
            step={0.1}
            marks
            valueLabelDisplay="auto"
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default BeamInput;
