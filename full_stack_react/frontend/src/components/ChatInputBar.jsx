// ChatInputBar.jsx
import React, { useState } from 'react';
import { Box, IconButton, TextField } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

export default function ChatInputBar({ onSend }) {
    const [inputValue, setInputValue] = useState('');

    const handleChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleSendClick = () => {
        if (!inputValue.trim()) return;
        onSend(inputValue);
        setInputValue('');
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendClick();
        }
    };

    return (
        <Box
            sx={{
                display: 'flex',
                alignItems: 'center',
                p: 1,
                borderRadius: '999px',
                backgroundColor: '#fff',
                boxShadow: 2,
            }}
        >
            <TextField
                variant="standard"
                placeholder="Type your message..."
                value={inputValue}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
                fullWidth
                InputProps={{
                    disableUnderline: true,
                    sx: {
                        fontSize: '1rem',
                        ml: 1,
                    },
                }}
            />
            <IconButton
                onClick={handleSendClick}
                sx={{
                    backgroundColor: '#1976d2',  // Votre bleu habituel
                    color: '#fff',
                    '&:hover': { backgroundColor: '#1565c0' },
                    ml: 1,
                    borderRadius: '50%',
                    width: 40,
                    height: 40,
                }}
            >
                <SendIcon />
            </IconButton>
        </Box>
    );
}
