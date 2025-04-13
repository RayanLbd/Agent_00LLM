// MiniGameScreen.jsx
import React from 'react';
import { Box, Typography } from '@mui/material';
import MiniJeu from './MiniJeu'; // Assurez-vous du bon chemin

const MiniGameScreen = () => {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                minHeight: '100vh',
                alignItems: 'center',
                justifyContent: 'space-between'
            }}
        >
            {/* Partie supérieure : le mini-jeu */}
            <Box sx={{ mt: 4 }}>
                <MiniJeu />
            </Box>

            {/* Footer fixe */}
            <Box sx={{ py: 2, width: '100%', textAlign: 'center', backgroundColor: '#F9FAFB' }}>
                <Typography
                    variant="h6"
                    sx={{
                        animation: 'loadingText 1.5s ease infinite',
                        color: '#777', // Couleur de base, qui passera en animation
                    }}
                >
                    Waiting for Voyager to find your dream trip...
                </Typography>
            </Box>
        </Box>
    );
};

export default MiniGameScreen;
