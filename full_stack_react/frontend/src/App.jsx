import React, { useEffect, useState } from 'react';
import { Box, Fade, CircularProgress, Typography } from '@mui/material';
import InitialScreen from './InitialScreen';
import ChatScreen from './ChatScreen';
import TripPreview from './TripPreview0';
import ConfirmationScreen from './ConfirmationScreen';
import { v4 as uuidv4 } from 'uuid';


// TODO: 
// 1. Front du chat cohérent -> OK
// 2. Images 
// 3. Cohérence du prix global 
// 4. Intégration TripAdvisor
// 5. Intégration météo 
// 6. Vol retour -> OK
// 7. Travel Map 

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [showChat, setShowChat] = useState(false);
  const [showWaitingScreen, setShowWaitingScreen] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [tripData, setTripData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const id = uuidv4();
    setSessionId(id);
  }, []);

  if (!sessionId) {
    return (
      <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <CircularProgress />
      </Box>
    );
  }

  // Fonction pour lancer la planification initiale
  const handlePlanTrip = async (initialInput) => {
    setLoading(true);
    try {
      // Envoyer la première requête avec le message de l'utilisateur
      const response = await fetch(`http://localhost:8000/chat?session_id=${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: initialInput })
      });
      const data_raw = await response.json();
      const assistantOutput = data_raw.assistant;
      console.log("Trip data received:", assistantOutput);

      // On suppose que la réponse contient l'objet mis à jour incluant l'historique complet
      if (assistantOutput.messages) {
        setMessages(assistantOutput.messages);
      } else {
        setMessages([
          { role: 'user', content: initialInput },
          { role: 'assistant', content: assistantOutput }
        ]);
      }
      setTripData(assistantOutput);
      setShowChat(true);
      setShowWaitingScreen(false);
    } catch (error) {
      console.error("Error fetching trip data:", error);
      setShowWaitingScreen(true);
    } finally {
      setLoading(false);
    }
  };

  // Fonction d'envoi d'un message dans le chat
  const handleSend = async (text) => {
    // Afficher immédiatement le message de l'utilisateur
    const newUserMsg = { role: 'user', content: text };
    setMessages(prev => [...prev, newUserMsg]);
    const thinkingMsg = { role: 'assistant', content: 'Voyager is thinking...', loading: true };
    setMessages(prev => [...prev, thinkingMsg]);
    try {
      // Envoyer uniquement le nouveau message (et session_id) au back-end
      const response = await fetch(`http://localhost:8000/chat?session_id=${sessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: text })
      });
      const data_raw = await response.json();
      const assistantOutput = data_raw.assistant;
      console.log("Assistant response: ", assistantOutput);
      // Ajouter la réponse de l'assistant à la conversation
      try {
        const lastMessage = assistantOutput.messages[assistantOutput.messages.length - 1];
        const newAssistantMsg = { role: 'assistant', content: lastMessage.content };
        setMessages(prev => prev.filter(msg => !msg.loading).concat(newAssistantMsg));
      } catch (error) {
        console.error("Error processing assistant message:", error);
      }
      setTripData(assistantOutput);
    } catch (error) {
      console.error("Error sending chat message:", error);
    }
  };

  const handleReserve = () => {
    setShowConfirmation(true);
  };

  const handleConfirmationClose = () => {
    setShowConfirmation(false);
    setShowChat(false);
  };

  console.log("tripData:", tripData);

  return (
    <Box sx={{ minHeight: '100vh', position: 'relative' }}>

      {/* Écran initial */}
      {!showChat && !showWaitingScreen && (
        <Fade in={!showChat} timeout={500}>
          <Box>
            <InitialScreen onSubmit={handlePlanTrip} />
            {loading && (
              <Box
                sx={{
                  position: 'absolute',
                  top: '50%',
                  left: '50%',
                  transform: 'translate(-50%, -50%)'
                }}
              >
                <CircularProgress />
              </Box>
            )}
          </Box>
        </Fade>
      )}

      {/* Écran d'attente en cas d'erreur ou absence d'historique */}
      {showWaitingScreen && (
        <Fade in={showWaitingScreen} timeout={500}>
          <Box
            sx={{
              display: 'flex',
              minHeight: '100vh',
              alignItems: 'center',
              justifyContent: 'center',
              flexDirection: 'column'
            }}
          >
            <CircularProgress />
            <Typography variant="h6" mt={2}>
              Still waiting to organize your dream trip...
            </Typography>
          </Box>
        </Fade>
      )}

      {/* Écran de chat et aperçu du voyage */}
      {showChat && (
        <Fade in={showChat} timeout={500}>
          <Box sx={{ display: 'flex', height: '100vh' }}>
            {/* Colonne Chat */}
            <Box
              sx={{
                width: { xs: '100%', md: 450 },
                borderRight: { xs: 'none', md: '1px solid #eee' },
                display: 'flex',
                flexDirection: 'column',
                overflowY: 'auto',
                overflowX: 'hidden'
              }}
            >
              <ChatScreen messages={messages} onSend={handleSend} />
            </Box>

            {/* Colonne de droite : aperçu du voyage */}
            <Box
              sx={{
                flex: 1,
                display: { xs: 'none', md: 'flex' },
                flexDirection: 'column',
                backgroundColor: '#F9FAFB',
                alignItems: 'center',
                justifyContent: 'center',
                px: 3,
                py: 1,
                overflowY: 'auto'
              }}
            >
              <TripPreview tripData={tripData.interface} onReserve={handleReserve} />
            </Box>
          </Box>
        </Fade>
      )}

      {/* Écran de confirmation */}
      {showConfirmation && (
        <Fade in={showConfirmation} timeout={500}>
          <ConfirmationScreen onClose={handleConfirmationClose} />
        </Fade>
      )}
    </Box>

  );
}

export default App;
