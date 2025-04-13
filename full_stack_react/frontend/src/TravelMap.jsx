import React from 'react';
import { Box } from '@mui/material';
import TransportMapArc from './TransportMapArc';

function TravelMap() {
    return (
        <Box
            sx={{
                width: '100%',
                height: 250, // Hauteur fixée, ajustable selon vos besoins
                border: '1px solid #ddd',
                borderRadius: 2,
                overflow: 'hidden'
            }}
        >
            <TransportMapArc />
        </Box>
    );
}

export default TravelMap;
