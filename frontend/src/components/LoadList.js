import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  Button,
  Box,
  Chip,
  Divider
} from '@mui/material';

const LoadList = ({ loads, onClearLoads }) => {
  const formatLoad = (load, type) => {
    switch (type) {
      case 'point_moments':
        return `${load.magnitude} N⋅m at ${load.location} m`;
      case 'point_forces':
        return `${load.magnitude} N at ${load.location} m`;
      case 'constant_force_profiles':
        return `${load.magnitude} N/m from ${load.start_location} m to ${load.end_location} m`;
      case 'triangular_force_profiles':
        return `${load.magnitude} N from ${load.start_location} m to ${load.end_location} m`;
      default:
        return 'Unknown load';
    }
  };

  const getLoadTypeLabel = (type) => {
    switch (type) {
      case 'point_moments':
        return 'Point Moments';
      case 'point_forces':
        return 'Point Forces';
      case 'constant_force_profiles':
        return 'Constant Force Profiles';
      case 'triangular_force_profiles':
        return 'Triangular Force Profiles';
      default:
        return 'Unknown';
    }
  };

  const getLoadTypeColor = (type) => {
    switch (type) {
      case 'point_moments':
        return 'primary';
      case 'point_forces':
        return 'secondary';
      case 'constant_force_profiles':
        return 'success';
      case 'triangular_force_profiles':
        return 'warning';
      default:
        return 'default';
    }
  };

  const totalLoads = Object.values(loads).reduce((sum, loadArray) => sum + loadArray.length, 0);

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            Current Loads ({totalLoads})
          </Typography>
          {totalLoads > 0 && (
            <Button 
              variant="outlined" 
              color="error" 
              size="small"
              onClick={onClearLoads}
            >
              Clear All
            </Button>
          )}
        </Box>

        {totalLoads === 0 ? (
          <Typography color="textSecondary" sx={{ textAlign: 'center', py: 2 }}>
            No loads added yet
          </Typography>
        ) : (
          <List dense>
            {Object.entries(loads).map(([loadType, loadArray]) => 
              loadArray.length > 0 && (
                <Box key={loadType}>
                  <Typography variant="subtitle2" sx={{ mt: 1, mb: 1 }}>
                    <Chip 
                      label={getLoadTypeLabel(loadType)} 
                      size="small" 
                      color={getLoadTypeColor(loadType)}
                      sx={{ mr: 1 }}
                    />
                    ({loadArray.length})
                  </Typography>
                  {loadArray.map((load, index) => (
                    <ListItem key={`${loadType}-${index}`} sx={{ pl: 2 }}>
                      <ListItemText 
                        primary={formatLoad(load, loadType)}
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItem>
                  ))}
                  {Object.keys(loads).indexOf(loadType) < Object.keys(loads).length - 1 && 
                   loadArray.length > 0 && <Divider sx={{ my: 1 }} />}
                </Box>
              )
            )}
          </List>
        )}
      </CardContent>
    </Card>
  );
};

export default LoadList;
