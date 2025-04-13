import React, { useEffect, useState } from 'react';

export default function TripAdvisorFetcher() {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPhotos = async () => {
            // Remplacez 'YOUR_API_KEY' par votre véritable clé API ou configurez-la dans l'environnement
            const apiKey = '0338B6D0C2B14D9E8FB4AA7E47D838FE';
            // Exemple d'URL avec un identifiant de location réel (ici "386919")
            const url = `https://api.content.tripadvisor.com/api/v1/location/386919/photos?language=en&key=${apiKey}`;
            const headers = { accept: "application/json" };

            try {
                const response = await fetch(url, { headers });
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const jsonData = await response.json();
                setData(jsonData);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchPhotos();
    }, []);

    return (
        <div style={{ padding: "1rem" }}>
            <h2>TripAdvisor API Test</h2>
            {error && <div style={{ color: "red" }}>Error: {error}</div>}
            {data ? (
                <pre>{JSON.stringify(data, null, 2)}</pre>
            ) : (
                <div>Loading photos...</div>
            )}
        </div>
    );
}
