import React from 'react';
import { Box, List, ListItem, ListItemAvatar, Avatar, Typography } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import agentAvatar from './image.png'; // Avatar de l'assistant
import userAvatar from './user.png';   // Avatar de l'utilisateur
import ChatInputBar from './components/ChatInputBar';

function ChatScreen({ messages, onSend }) {
    return (
        <Box
            sx={{
                width: '450px',
                minHeight: '100vh',
                backgroundColor: '#fff',
                display: 'flex',
                flexDirection: 'column',
                boxShadow: 4,
            }}
        >
            {/* En-tête */}
            <Box sx={{ p: 2, borderBottom: '1px solid #eee' }}>
                <ReactMarkdown
                    components={{
                        p: ({ node, ...props }) => <Box component="span" {...props} />,
                    }}
                >
                    **Voyager, your AI travel assistant**
                </ReactMarkdown>
            </Box>

            {/* Liste des messages */}
            <Box sx={{ flex: 1, overflowY: 'auto', p: 0 }}>
                <List sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                    {messages.map((msg, idx) => {
                        // Si le message est en chargement, on l'affiche différemment
                        if (msg.loading) {
                            return (
                                <ListItem key={idx} sx={{ justifyContent: 'center' }}>
                                    <Typography
                                        variant="body2"
                                        sx={{
                                            animation: 'loadingText 1.5s ease infinite',
                                            textAlign: 'center'
                                        }}
                                    >
                                        {msg.content}
                                    </Typography>
                                </ListItem>
                            );
                        }
                        // Rendu classique pour les autres messages
                        const isAssistant = msg.role === 'assistant';
                        return (
                            <ListItem
                                key={idx}
                                sx={{
                                    display: 'flex',
                                    flexDirection: isAssistant ? 'row' : 'row-reverse',
                                    alignItems: 'flex-start',
                                }}
                            >
                                <ListItemAvatar sx={{ minWidth: '40px' }}>
                                    <Avatar src={isAssistant ? agentAvatar : userAvatar} />
                                </ListItemAvatar>
                                <Box
                                    sx={{
                                        backgroundColor: isAssistant ? '#f1f1f1' : '#d1e7dd',
                                        borderRadius: 2,
                                        p: 2,
                                        maxWidth: '70%',
                                        boxShadow: 1,
                                    }}
                                >
                                    <ReactMarkdown
                                        components={{
                                            a: ({ node, ...props }) => (
                                                <a
                                                    {...props}
                                                    style={{ color: '#1976d2', textDecoration: 'underline' }}
                                                />
                                            ),
                                            strong: ({ node, ...props }) => <strong {...props} />,
                                            p: ({ node, ...props }) => <p style={{ margin: 0 }} {...props} />,
                                        }}
                                    >
                                        {msg.content}
                                    </ReactMarkdown>
                                </Box>
                            </ListItem>
                        );
                    })}
                </List>
            </Box>

            {/* Zone d'entrée */}
            <Box sx={{ mb: 2, px: 2 }}>
                <ChatInputBar onSend={onSend} />
            </Box>
        </Box>
    );
}

export default ChatScreen;
