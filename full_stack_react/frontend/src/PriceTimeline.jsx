import React, { useState, useEffect } from 'react';
import { Box, Typography, Chip, Stack, Divider } from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';

function PriceTimeline({
    days,
    price,
    dateRange,
    daysCount,
    nightsCount,
    passengers = { adults: 2, children: 1 },
    selectedTimeline,      // Optionnel : sélection initiale (ex. "✨ Summary")
    onSelectTimeline       // Callback appelé quand l'utilisateur clique sur une chip
}) {
    // Si selectedTimeline n'est pas fourni, on démarre avec "✨ Summary"
    const [selectedChip, setSelectedChip] = useState(selectedTimeline || "✨ Summary");

    // Synchronisation si la prop selectedTimeline change en cours de route
    useEffect(() => {
        if (selectedTimeline && selectedTimeline !== selectedChip) {
            setSelectedChip(selectedTimeline);
        }
    }, [selectedTimeline, selectedChip]);

    // On ajoute "✨ Summary" devant les jours
    const timelineOptions = ["✨ Summary", ...days];

    const handleChipClick = (option) => {
        setSelectedChip(option);
        if (onSelectTimeline) {
            onSelectTimeline(option);
        }
    };

    return (
        <Box sx={{ border: '1px solid #ddd', borderRadius: 2, p: 2 }}>
            {/* Prix & période */}
            {price &&
                <Box sx={{ display: 'flex', alignItems: 'baseline', mb: 1 }}>
                    <Typography variant="h6" fontWeight="bold" sx={{ mr: 1 }}>
                        € {price}
                    </Typography>
                    {dateRange &&
                        <Typography variant="body2" color="text.secondary">
                            {dateRange}
                        </Typography>}
                </Box>}

            {/* TTC price per person */}
            {price && <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                TTC price per person
            </Typography>}

            {/* Nombre de jours et nuits */}
            {daysCount && nightsCount ? (
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <CalendarMonthIcon fontSize="small" sx={{ mr: 0.5 }} />

                    <Typography variant="body2" color="text.secondary">
                        {daysCount} days, {nightsCount} nights
                    </Typography>
                </Box>) : null}

            {/* Passagers */}
            {passengers &&
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <PersonIcon fontSize="small" sx={{ mr: 0.5 }} />
                    <Typography variant="body2" color="text.secondary">
                        {passengers.adults} adults, {passengers.children} child
                    </Typography>
                </Box>}

            <Divider sx={{ mb: 1 }} />

            {/* Timeline avec wrap */}
            <Stack
                direction="row"
                sx={{
                    flexWrap: 'wrap',
                    rowGap: 1,
                    columnGap: 1
                }}
            >
                {timelineOptions.map((option, index) => (
                    <Chip
                        key={index}
                        label={option}
                        color={selectedChip === option ? 'primary' : 'default'}
                        onClick={() => handleChipClick(option)}
                    />
                ))}
            </Stack>
        </Box>
    );
}

export default PriceTimeline;
