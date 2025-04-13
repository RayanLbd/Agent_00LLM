import React, { useState } from 'react';
import {
    Box,
    Button,
    Typography,
    TextField,
    Chip,
    Paper,
    Avatar,
    Container
} from '@mui/material';
import { styled } from '@mui/system';
import agentAvatar from './image.png'; // Ajuste le chemin si nécessaire

// Gradient de fond
const Background = styled(Box)({
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #36D1DC 0%, #5B86E5 100%)'
});

function InitialScreen({ onSubmit }) {
    const [initialInput, setInitialInput] = useState('');

    const handleChipClick = (value) => {
        setInitialInput(value);
    };

    const handleSubmit = () => {
        if (!initialInput.trim()) return;
        onSubmit(initialInput);
    };

    return (
        <Background>
            <Container maxWidth="sm">
                <Paper
                    elevation={4}
                    sx={{
                        p: 4,
                        borderRadius: 3,
                        textAlign: 'center'
                    }}
                >
                    {/* Avatar de la mascotte */}
                    <Avatar
                        src={agentAvatar}
                        alt="Agent Avatar"
                        sx={{
                            width: 100,
                            height: 100,
                            mx: 'auto',
                            mb: 2,
                            boxShadow: 3,
                            transition: 'box-shadow 0.3s ease',
                            '&:hover': {
                                boxShadow: '0 0 15px rgba(0, 0, 0, 0.5)'
                            }
                        }}
                    />

                    <Typography variant="h4" fontWeight="bold" gutterBottom>
                        Where do you want to go?
                    </Typography>
                    <Typography variant="subtitle1" color="grey.600" gutterBottom>
                        And in what mood?
                    </Typography>
                    <Typography variant="body2" color="grey.500" gutterBottom>
                        Your personal AI travel companion
                    </Typography>

                    {/* Champ de saisie */}
                    <TextField
                        variant="outlined"
                        placeholder="I want to go to the sun"
                        value={initialInput}
                        onChange={(e) => setInitialInput(e.target.value)}
                        fullWidth
                        sx={{ mt: 3 }}
                    />

                    {/* Suggestions (chips) */}
                    <Box
                        sx={{
                            display: 'flex',
                            gap: 1,
                            justifyContent: 'center',
                            mt: 2,
                            flexWrap: 'wrap'
                        }}
                    >
                        {['beach', 'sun', 'next week'].map((label) => (
                            <Chip
                                key={label}
                                label={label}
                                variant="outlined"
                                onClick={() => {
                                    if (label === 'beach') {
                                        handleChipClick('I want a beach holiday');
                                    } else if (label === 'sun') {
                                        handleChipClick('I want to go to the sun');
                                    } else {
                                        handleChipClick('I want to travel next week');
                                    }
                                }}
                                sx={{
                                    transition: 'background-color 0.3s ease',
                                    '&:hover': {
                                        backgroundColor: 'rgba(0,0,0,0.05)'
                                    }
                                }}
                            />
                        ))}
                    </Box>

                    {/* Bouton CTA */}
                    <Button
                        variant="contained"
                        sx={{
                            mt: 3,
                            px: 4,
                            py: 1.2,
                            borderRadius: '999px',
                            backgroundColor: '#FB8C00',
                            textTransform: 'none',
                            fontWeight: 'bold',
                            boxShadow: 2,
                            transition: 'background-color 0.3s ease, box-shadow 0.3s ease',
                            '&:hover': {
                                backgroundColor: '#F57C00',
                                boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
                            }
                        }}
                        onClick={handleSubmit}
                    >
                        Plan My Trip
                    </Button>
                </Paper>
            </Container>
        </Background>
    );
}

export default InitialScreen;
