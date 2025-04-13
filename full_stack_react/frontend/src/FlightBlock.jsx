import React from "react";
import { Box, Typography, Divider, Stack } from "@mui/material";
import FlightIcon from "@mui/icons-material/Flight";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import BusinessCenterIcon from "@mui/icons-material/BusinessCenter";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import WorkIcon from "@mui/icons-material/Work"; // ex. pour bagage

function FlightDetails({ flight, label }) {
    /**
     * flight = {
     *   fromCity: "Paris",
     *   toCity: "Faro",
     *   departureTime: "08:00",
     *   duration: "2h40",
     *   airline: "Air Portugal",
     *   flightClass: "Economy",
     *   fromAirport: "Paris-Orly (ORY)",
     *   toAirport: "Faro (FAO)",
     *   baggage: "1 cabin bag + 1 checked bag included"
     * }
     * label = "(Outbound)" ou "(Return)"
     */

    return (
        <Box sx={{ mb: 2 }}>
            {/* Titre : Flight: Paris → Faro (Outbound) */}
            <Typography variant="body1" fontWeight="bold" sx={{ mb: 1 }}>
                Flight: {flight.fromCity} → {flight.toCity}{" "}
                <Typography
                    component="span"
                    variant="body2"
                    color="text.secondary"
                    sx={{ ml: 1 }}
                >
                    {label}
                </Typography>
            </Typography>

            {/* Departure time + duration */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <AccessTimeIcon fontSize="small" color="primary" sx={{ mr: 1 }} />
                <Typography variant="body2" color="text.secondary">
                    Departure: {flight.departureTime} — Duration: {flight.duration}
                </Typography>
            </Box>

            {/* Airline + class */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <BusinessCenterIcon fontSize="small" color="primary" sx={{ mr: 1 }} />
                <Typography variant="body2" color="text.secondary">
                    Airline: {flight.airline}, {flight.flightClass}
                </Typography>
            </Box>

            {/* Airport info */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <LocationOnIcon fontSize="small" color="primary" sx={{ mr: 1 }} />
                <Typography variant="body2" color="text.secondary">
                    Airport: {flight.fromAirport} → {flight.toAirport}
                </Typography>
            </Box>

            {/* Baggage */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <WorkIcon fontSize="small" color="primary" sx={{ mr: 1 }} />
                <Typography variant="body2" color="text.secondary">
                    Baggage: {flight.baggage}
                </Typography>
            </Box>
        </Box>
    );
}

function FlightBlock({ flightBlockData }) {
    // flightBlockData = {
    //   outbound: {...}, inbound: {...}
    // }
    return (
        <Box
            sx={{
                border: "1px solid #ddd",
                borderRadius: 2,
                p: 2
            }}
        >
            {/* Titre principal "Flights" avec l'icône avion en bleu */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <FlightIcon sx={{ mr: 1 }} />
                <Typography variant="h6">
                    Flights
                </Typography>
            </Box>
            <Divider sx={{ mb: 2 }} />

            {/* Deux colonnes : outbound, inbound */}
            <Stack direction="row" spacing={2}>
                <Box sx={{ flex: 1 }}>
                    {/* Outbound */}
                    {flightBlockData.outbound && <FlightDetails
                        flight={flightBlockData.outbound}
                        label="(Outbound)"
                    />}
                </Box>
                <Box sx={{ flex: 1 }}>
                    {/* Return */}
                    {flightBlockData.inbound &&
                        <FlightDetails
                            flight={flightBlockData.inbound}
                            label="(Return)"
                        />}
                </Box>
            </Stack>
        </Box>
    );
}

export default FlightBlock;
