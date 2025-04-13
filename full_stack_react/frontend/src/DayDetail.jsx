import React from 'react';
import { Box, Typography, Divider, Stack } from '@mui/material';
import FlightIcon from '@mui/icons-material/Flight';
import HotelIcon from '@mui/icons-material/Hotel';
import ActivitiesBlock from './ActivitiesBlock';
import FoodRecommendationsBlock from './FoodRecommendationsBlock';

function DayDetail({ dayData }) {
    return (
        <Box sx={{ p: 2 }}>
            {/* Titre de la journée */}
            {dayData.dayTitle && (
                <Typography variant="h6" fontWeight="bold" sx={{ mb: 2 }}>
                    {dayData.dayTitle}
                </Typography>
            )}

            {/* Section Vol & Hôtel minimal */}
            <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
                {dayData.flight && (
                    <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
                        <FlightIcon color="primary" sx={{ mr: 0.5 }} />
                        <Typography variant="body2">
                            {dayData.flight.from} → {dayData.flight.to} at {dayData.flight.time}
                        </Typography>
                    </Box>
                )}
                {/* L'hôtel s'affiche toujours */}
                <Box sx={{ display: 'flex', alignItems: 'center', flex: 1 }}>
                    <HotelIcon color="primary" sx={{ mr: 0.5 }} />
                    <Typography variant="body2" >
                        {dayData.hotel ? `${dayData.hotel.name} – ${dayData.hotel.nights} nights` : "Hotel info unavailable"}
                    </Typography>
                </Box>
            </Stack>

            <Divider sx={{ mb: 2 }} />

            {/* Description de la journée */}
            {dayData.dayDescription && (
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                    {dayData.dayDescription}
                </Typography>
            )}

            <Box sx={{ flex: 0.75, display: 'flex', flexDirection: 'column', gap: 2 }}>

                {/* Bloc Food Recommendations */}
                {dayData.foodRecommendations && dayData.foodRecommendations.length > 0 && (
                    <FoodRecommendationsBlock foodRecommendations={dayData.foodRecommendations} />
                )}

                {/* Bloc Activités (réutilise le même composant) */}
                {dayData.activities && dayData.activities.length > 0 && (
                    <ActivitiesBlock activities={dayData.activities} />
                )}
            </Box>
        </Box>
    );
}

export default DayDetail;
