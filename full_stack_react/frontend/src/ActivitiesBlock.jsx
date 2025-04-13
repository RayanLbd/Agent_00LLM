import React from "react";
import {
    Box,
    Typography,
    Divider,
    Card,
    CardMedia,
    CardContent,
    Chip,
    Link
} from "@mui/material";
import tripAdvisorLogo from "./tripAdvisor.png";
import LocalActivityIcon from '@mui/icons-material/LocalActivity';
import LinkIcon from "@mui/icons-material/Link";

function ActivityCard({ activity }) {
    return (
        <Card
            sx={{
                position: "relative",
                borderRadius: 2,
                overflow: "hidden",
                boxShadow: 2,
                width: "100%",
                maxWidth: 343,
                mb: 2
            }}
        >
            {/* Image */}
            <Box sx={{ position: "relative" }}>
                <CardMedia
                    component="img"
                    height="120"
                    image={activity.image}
                    alt={activity.title}
                />
                {/* Chip en bas à droite (vibe) */}
                {activity.vibe && (
                    <Chip
                        label={activity.vibe}
                        sx={{
                            position: "absolute",
                            bottom: 8,
                            right: 8,
                            // Fond pastel vert pour "Relaxed", pastel rouge pour "We love it!"
                            bgcolor:
                                activity.vibe === "Relaxed"
                                    ? "#a5d6a7" // vert pastel
                                    : activity.vibe === "We love it!"
                                        ? "#FFCDD2" // rouge pastel
                                        : "primary.main",
                            // color: "#fff",
                            borderRadius: 1
                        }}
                    />
                )}
                {/* Logo TripAdvisor + rating en haut à droite */}
                {activity.rating && (
                    <Box
                        sx={{
                            position: "absolute",
                            top: 8,
                            right: 8,
                            display: "flex",
                            alignItems: "center",
                            gap: 0.5,
                            bgcolor: "rgba(255,255,255,0.8)",
                            borderRadius: 1,
                            px: 1
                        }}
                    >
                        <Box
                            component="img"
                            src={tripAdvisorLogo}
                            alt="TripAdvisor"
                            sx={{ width: 16, height: 16 }}
                        />
                        <Typography variant="caption" sx={{ fontWeight: "bold" }}>
                            {activity.rating}
                        </Typography>
                    </Box>
                )}
            </Box>

            {/* Titre + description */}
            <CardContent sx={{ p: 1.5 }}>
                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between"
                    }}
                >
                    <Typography variant="subtitle1" fontWeight="bold" sx={{ mb: 0.5 }}>
                        {activity.title}
                    </Typography>
                    {activity.link && (
                        <Link
                            href={activity.link}
                            target="_blank"
                            rel="noopener"
                            sx={{ color: "primary.main" }}
                        >
                            <LinkIcon fontSize="small" />
                        </Link>
                    )}
                </Box>
                <Typography variant="body2" color="text.secondary" noWrap>
                    {activity.description}
                </Typography>
            </CardContent>
        </Card>
    );
}

export default function ActivitiesBlock({ activities }) {
    /**
     * activities = [
     *   {
     *     title: "Ponta da Piedade",
     *     description: "Explore the stunning rock formations...",
     *     rating: "4.5/5",
     *     vibe: "Relaxed",
     *     image: "algarve.png"
     *   },
     *   {
     *     title: "Welcome Dinner",
     *     description: "Enjoy a welcome dinner by the ocean...",
     *     rating: "4.8/5",
     *     vibe: "We love it!",
     *     image: "algarve.png"
     *   },
     *   ...
     * ]
     */
    const total = activities.length;
    return (
        <Box
            sx={{
                border: "1px solid #ddd",
                borderRadius: 2,
                p: 2
            }}
        >
            {/* Titre Activities avec un logo devant */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <LocalActivityIcon sx={{ mr: 1 }} />
                <Typography variant="h6">
                    Activities
                </Typography>
            </Box>
            <Divider sx={{ mb: 2 }} />

            {/* Grille "responsive" 
          - xs={12} => sur petit écran 1 colonne 
          - sm={6} => sur + grand écran 2 colonnes
          - si c'est le dernier item d'un total impair => on force 1 colonne en sm
      */}
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 2 }}>
                {activities.map((act, index) => {
                    const isLastAndOdd = (total % 2 === 1) && (index === total - 1);
                    return (
                        <Box
                            key={index}
                            sx={{
                                width: { xs: "100%", sm: isLastAndOdd ? "100%" : "calc(50% - 8px)" }
                            }}
                        >
                            <ActivityCard activity={act} />
                        </Box>
                    );
                })}
            </Box>
        </Box>
    );
}
