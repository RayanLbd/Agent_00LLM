import React, { useState } from 'react';
import {
    Box,
    CardMedia,
    Typography,
    Chip,
    Stack,
    Button,
    Divider,
    CardContent
} from '@mui/material';
import FlightIcon from '@mui/icons-material/Flight';
import HotelIcon from '@mui/icons-material/Hotel';
import MapIcon from '@mui/icons-material/Map';
import TransportMapArc from './TransportMapArc';

const mockTripData = {
    price: 680,
    dateRange: "May 9–13",
    location: "Algarve",
    nights: 4,
    days: [
        {
            dayLabel: "✨ Summary",
            flight: { from: "Paris", to: "Faro", time: "08:00" },
            hotel: { name: "Lagos Bay Resort", nights: 4 },
            activities: [
                { label: "Ponta da Piedade", description: "Enjoy scenic views." },
                { label: "Welcome Dinner", description: "Taste local cuisine." }
            ],
            route: "Paris → Faro"
        },
        {
            dayLabel: "Day 1",
            flight: { from: "Paris", to: "Faro", time: "08:00" },
            hotel: { name: "Lagos Bay Resort", nights: 4 },
            activities: [
                { label: "Ponta da Piedade", description: "Enjoy scenic views." },
                { label: "Welcome Dinner", description: "Taste local cuisine." }
            ],
            route: "Paris → Faro"
        },
        {
            dayLabel: "Day 2",
            flight: null,
            hotel: null,
            activities: [
                { label: "Beach Time", description: "Relax at the beach." },
                { label: "Local Market", description: "Explore local products." }
            ],
            route: "Local exploration"
        }
    ]
};

function TripPreview() {
    const [selectedDay, setSelectedDay] = useState(0);
    const dayData = mockTripData.days[selectedDay];

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
            {/* SECTION 1 : Header non scrollable */}
            <Box>
                <CardMedia
                    component="img"
                    height="160"
                    image="/algarve.jpg"
                    alt="Algarve"
                />
                <Box sx={{ p: 2 }}>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                        Here’s Your Perfect Trip to {mockTripData.location}, Planned for You
                    </Typography>
                    <Typography variant="h5" fontWeight="bold">
                        € {mockTripData.price}
                        <Typography component="span" variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                            {mockTripData.dateRange}
                        </Typography>
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {mockTripData.nights} nights
                    </Typography>
                    <Box
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            overflowX: 'auto',
                            mt: 1,
                            pb: 1
                        }}
                    >
                        {mockTripData.days.map((day, index) => (
                            <Chip
                                key={index}
                                label={day.dayLabel}
                                onClick={() => setSelectedDay(index)}
                                color={selectedDay === index ? 'primary' : 'default'}
                                sx={{ mr: 1, flexShrink: 0 }}
                            />
                        ))}
                    </Box>
                </Box>
            </Box>

            <Divider sx={{ mb: 1 }} />

            {/* SECTION 2 : Zone centrale scrollable (détails + carte) */}
            <Box
                sx={{
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'row',
                    gap: 2,
                    overflow: 'hidden'
                }}
            >
                {/* Colonne gauche : Détails scrollables */}
                <Box sx={{ flex: 1, overflowY: 'auto', p: 2 }}>
                    {dayData.flight && (
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <FlightIcon color="primary" sx={{ mr: 1 }} />
                            <Typography variant="body1">
                                Flight: {dayData.flight.from} → {dayData.flight.to} at {dayData.flight.time}
                            </Typography>
                        </Box>
                    )}
                    {dayData.hotel && (
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <HotelIcon color="primary" sx={{ mr: 1 }} />
                            <Typography variant="body1">
                                Hotel: {dayData.hotel.name} – {dayData.hotel.nights} nights
                            </Typography>
                        </Box>
                    )}
                    {dayData.route && (
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                            <MapIcon color="primary" sx={{ mr: 1 }} />
                            <Typography variant="body1">
                                Route: {dayData.route}
                            </Typography>
                        </Box>
                    )}
                    <Typography variant="body1" fontWeight="bold" sx={{ mb: 1 }}>
                        Activities:
                    </Typography>
                    <Stack direction="row" spacing={1} sx={{ flexWrap: 'wrap', mb: 2 }}>
                        {dayData.activities.map((activity, i) => (
                            <Box
                                key={i}
                                sx={{
                                    width: 100,
                                    borderRadius: 1,
                                    boxShadow: 1,
                                    overflow: 'hidden'
                                }}
                            >
                                <CardMedia
                                    component="img"
                                    height="60"
                                    image="/imageActi.jpg"
                                    alt={activity.label}
                                />
                                <Box sx={{ p: 0.5 }}>
                                    <Typography variant="body2" noWrap>
                                        {activity.label}
                                    </Typography>
                                </Box>
                            </Box>
                        ))}
                    </Stack>
                </Box>

                {/* Colonne droite : Carte interactive */}
                <Box
                    sx={{
                        flex: 1,
                        minWidth: 250,
                        display: 'flex',
                        alignItems: 'flex-start',
                        justifyContent: 'center',
                        p: 2
                    }}
                >
                    <Box sx={{ width: '100%', maxWidth: 400, height: 250 }}>
                        <TransportMapArc />
                    </Box>
                </Box>
            </Box>

            {/* SECTION 3 : Bouton CTA sticky en bas */}
            <Box
                sx={{
                    position: 'sticky',
                    bottom: 0,
                    borderTop: '1px solid #eee',
                    p: 2,
                    display: 'flex',
                    justifyContent: 'center'
                }}
            >
                <Button
                    variant="contained"
                    sx={{
                        borderRadius: '999px',
                        px: 3,
                        py: 1,
                        textTransform: 'none',
                        fontWeight: 'bold'
                    }}
                >
                    Je réserve ce voyage
                </Button>
            </Box>
        </Box>
    );
}

export default TripPreview;
