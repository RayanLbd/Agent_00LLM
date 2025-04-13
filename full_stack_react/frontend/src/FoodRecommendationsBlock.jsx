import React from "react";
import { Box, Typography, Paper, CardMedia, Divider } from "@mui/material";
import RestaurantIcon from '@mui/icons-material/Restaurant';

function FoodRecommendationsBlock({ foodRecommendations }) {
    return (
        <Box sx={{ border: "1px solid #ddd", borderRadius: 2, p: 2, mt: 2 }}>
            {/* Titre avec logo */}
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <RestaurantIcon sx={{ mr: 1 }} />
                <Typography variant="h6">
                    Food Recommendations
                </Typography>
            </Box>
            <Divider sx={{ mb: 2 }} />
            {/* Conteneur en flex pour obtenir deux colonnes 50/50 */}
            <Box sx={{ display: "flex", gap: 2 }}>
                {foodRecommendations.slice(0, 2).map((food, index) => (
                    <Paper
                        key={index}
                        variant="outlined"
                        sx={{
                            flex: 1,
                            p: 1,
                            display: "flex",
                            alignItems: "center",
                            gap: 1
                        }}
                    >
                        <CardMedia
                            component="img"
                            sx={{ width: 60, height: 60, borderRadius: 1 }}
                            image={food.image}
                            alt={food.title}
                        />
                        <Box>
                            <Typography variant="subtitle2" fontWeight="bold" noWrap>
                                {food.title}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                                {food.description}
                            </Typography>
                        </Box>
                    </Paper>
                ))}
            </Box>
        </Box>
    );
}

export default FoodRecommendationsBlock;
