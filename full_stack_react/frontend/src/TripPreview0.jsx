import React, { useState } from 'react';
import {
    Box,
    CardMedia,
    Typography,
    Divider,
    Button,
    Fade
} from '@mui/material';
import PriceTimeline from './PriceTimeline';
import TravelMap from './TravelMap';
import FlightBlock from './FlightBlock';
import HotelBlock from './HotelBlock';
import ActivitiesBlock from './ActivitiesBlock';
import DayDetail from './DayDetail'; // Composant pour la vue détaillée d'un jour

function TripPreview({ tripData }) {
    // selectedTimeline gère la sélection dans PriceTimeline : "Summary" ou "Day 1", "Day 2", etc.

    const [selectedTimeline, setSelectedTimeline] = useState("✨ Summary");
    if (!tripData.location) {
        console.log("Données du voyage incomplètes : ", tripData);
        return <div>Données du voyage incomplètes ...</div>;
    }

    // Pour les vues détaillées, calculer l'index en retirant "Day " du label (ex: "Day 1" -> 0)


    // Récupérer les données du jour sélectionné
    const tripData_days = tripData.days && tripData.days.length > 0 ? tripData.days : [];
    console.log("tripData_days: ", tripData_days);
    const selectedDayIndex =
        selectedTimeline === "✨ Summary"
            ? 0
            : parseInt(selectedTimeline.replace("Day ", "")) - 1;
    let dayData = null;
    if (tripData_days.length > 0) {
        dayData = tripData_days[selectedDayIndex];
    }
    // Pour le résumé, on utilisera les données générales (du premier jour par défaut)
    const summaryFlightData = tripData.flightBlockData;
    const summaryHotelData = tripData.hotelData;
    const summaryActivities = tripData.topActivities;
    return (
        <Box
            sx={{
                width: '100%',
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden'
            }}
        >
            {/* SECTION 1 : Image du voyage */}
            <Box>
                <CardMedia
                    component="img"
                    height="200"
                    image="/algarve.jpg"
                    alt="Trip main"
                />
            </Box>

            {/* SECTION 2 : Titre principal */}
            <Box sx={{ p: 2 }}>
                <Typography variant="h5" fontWeight="bold">
                    Here’s Your Perfect Trip to {tripData.location}, Planned for You
                </Typography>
            </Box>

            <Divider />

            {/* SECTION 3 : Contenu principal en deux colonnes - scroll unifié */}
            <Box
                sx={{
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'row',
                    gap: 2,
                    overflowY: 'auto',
                    '&::-webkit-scrollbar': { width: '6px' },
                    '&::-webkit-scrollbar-thumb': {
                        backgroundColor: 'rgba(0,0,0,0.2)',
                        borderRadius: '3px'
                    },
                    p: 2
                }}
            >
                {/* Colonne gauche (environ 25% de l'espace) */}
                <Box sx={{ flex: 0.25, display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <PriceTimeline
                        days={tripData_days.map(day => day.dayLabel)}
                        price={tripData.price}
                        dateRange={tripData.dateRange}
                        daysCount={tripData_days.length}
                        nightsCount={tripData.nights}
                        passengers={tripData.passengers}
                        selectedTimeline={selectedTimeline}
                        onSelectTimeline={setSelectedTimeline}
                    />
                    <Box>
                        <Typography variant="h6" sx={{ mb: 1 }}>
                            Travel Map
                        </Typography>
                        <TravelMap />
                    </Box>
                </Box>

                {/* Colonne droite (environ 75% de l'espace) */}
                <Box sx={{ flex: 0.75, display: 'flex', flexDirection: 'column', gap: 2 }}>
                    {selectedTimeline === "✨ Summary" ? (
                        <>
                            {(summaryFlightData &&
                                <FlightBlock flightBlockData={tripData.flightBlockData} />
                            )}
                            {(summaryHotelData &&
                                <HotelBlock hotelData={tripData.hotelData} />
                            )}
                            {(summaryActivities &&
                                <ActivitiesBlock activities={summaryActivities} />
                            )}
                        </>
                    ) : (dayData && (<DayDetail dayData={dayData} />)

                    )}
                </Box>
            </Box>

            {/* SECTION 4 : Bouton CTA sticky en bas */}
            <Box
                sx={{
                    position: 'sticky',
                    bottom: 0,
                    width: '100%',
                    p: 2,
                    borderTop: '1px solid #eee',
                    display: 'flex',
                    justifyContent: 'center'
                }}
            >
                <Button
                    variant="contained"
                    sx={{
                        borderRadius: '999px',
                        textTransform: 'none',
                        fontWeight: 'bold',
                        px: 4,
                        py: 1,
                        maxWidth: 400,
                        width: '100%'
                    }}
                >
                    Je réserve ce voyage
                </Button>
            </Box>
        </Box>
    );
}

export default TripPreview;
