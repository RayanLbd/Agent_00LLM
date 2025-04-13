import React from "react";
import {
    Box,
    Typography,
    Divider,
    Stack,
    Link
} from "@mui/material";

// Quelques icônes MUI
import HotelIcon from "@mui/icons-material/Hotel";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import StarIcon from "@mui/icons-material/Star";
import SpaIcon from "@mui/icons-material/Spa";
import PoolIcon from "@mui/icons-material/Pool";
import WorkIcon from "@mui/icons-material/Work"; // ex. bagage or something
import LinkIcon from "@mui/icons-material/Link";
import MapIcon from "@mui/icons-material/Map";

function HotelBlock({ hotelData }) {
    /**
     * hotelData = {
     *   name: "Lagos Bay Resort",
     *   nights: 4,
     *   rating: 4.6,
     *   reviewsCount: 1352,
     *   location: "Lagos, Algarve, Portugal",
     *   amenities: ["Pool", "Spa", "Breakfast included", "Ocean view"],
     *   room: "Deluxe Suite with Balcony",
     *   website: "https://www.lagosbayresort.com",
     *   mapLink: "https://maps.google.com/..."
     * }
     */

    const {
        name,
        nights,
        rating,
        reviewsCount,
        location,
        amenities,
        room,
        website,
        mapLink
    } = hotelData;

    return (
        <Box
            sx={{
                border: "1px solid #ddd",
                borderRadius: 2,
                p: 2
            }}
        >
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <HotelIcon sx={{ mr: 1 }} />
                <Typography variant="h6">
                    Hotels
                </Typography>
            </Box>
            <Divider sx={{ mb: 2 }} />

            {/* Hotel + nights */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <Typography variant="body1" fontWeight="bold">
                    {name} – {nights} nights
                </Typography>
            </Box>

            {/* Rating */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <StarIcon fontSize="small" sx={{ mr: 1 }} color="primary" />
                <Typography variant="body2" color="text.secondary">
                    Rating: {rating} / 5 (based on {reviewsCount ? reviewsCount.toLocaleString() : "N/A"} reviews)
                </Typography>
            </Box>

            {/* Location */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <LocationOnIcon fontSize="small" sx={{ mr: 1 }} color="primary" />
                <Typography variant="body2" color="text.secondary">
                    Location: {location}
                </Typography>
            </Box>

            {/* Amenities */}
            {amenities && amenities.length > 0 && (
                <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                    <PoolIcon fontSize="small" sx={{ mr: 1 }} color="primary" />
                    <Typography variant="body2" color="text.secondary">
                        Amenities: {amenities.join(", ")}
                    </Typography>
                </Box>
            )}

            {/* Room */}
            {room && (
                <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                    <HotelIcon fontSize="small" sx={{ mr: 1 }} color="primary" />
                    <Typography variant="body2" color="text.secondary">
                        Room: {room}
                    </Typography>
                </Box>
            )}

            {/* Liens : Visit website + View on maps, séparés par un | */}
            <Box sx={{ display: "flex", alignItems: "center", mt: 1, gap: 2 }}>
                {website && (
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <LinkIcon fontSize="small" color="primary" />
                        <Link
                            href={website}
                            target="_blank"
                            rel="noopener"
                            underline="hover"
                        >
                            Visit hotel website
                        </Link>
                    </Box>
                )}
                {/* On met le '|' si on a les deux liens */}
                {website && mapLink && <Typography variant="body2" color="text.secondary">|</Typography>}

                {mapLink && (
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <MapIcon fontSize="small" color="primary" />
                        <Link
                            href={mapLink}
                            target="_blank"
                            rel="noopener"
                            underline="hover"
                        >
                            View on map
                        </Link>
                    </Box>
                )}
            </Box>
        </Box>
    );
}

export default HotelBlock;
