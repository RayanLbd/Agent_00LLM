import React from 'react';
import { Box, Typography, Button } from '@mui/material';

function ConfirmationScreen({ onClose }) {
    return (
        <Box
            sx={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                bgcolor: 'rgba(0,0,0,0.5)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                zIndex: 9999,
            }}
        >
            <Box
                sx={{
                    backgroundColor: '#fff',
                    borderRadius: 2,
                    p: 3,
                    maxWidth: 400,
                    width: '90%',
                    textAlign: 'center',
                }}
            >
                <Box
                    component="img"
                    src="/image.png"
                    alt="Confirmation"
                    sx={{ width: 80, height: 80, mb: 2 }}
                />
                <Typography variant="h6" fontWeight="bold" sx={{ mb: 1 }}>
                    Your trip has been reserved!
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    You’ll receive a confirmation email shortly.
                </Typography>
                <Button
                    variant="contained"
                    onClick={onClose}
                    sx={{
                        borderRadius: '999px',
                        textTransform: 'none',
                        fontWeight: 'bold',
                        px: 4,
                        py: 1,
                        backgroundColor: '#1976d2'
                    }}
                >
                    OK
                </Button>
            </Box>
        </Box>
    );
}

export default ConfirmationScreen;
