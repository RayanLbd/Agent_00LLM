const mockTripData = {
    price: 680,
    dateRange: "May 9–13",
    location: "Algarve",
    nights: 4,
    passengers: { adults: 2, children: 1 },
    days: [
        {
            dayLabel: "Day 1",
            date: "2025-05-09",
            dayTitle: "Day 1: Arrival and Exploration",
            dayDescription: "Upon arrival in Faro, enjoy a scenic drive and settle into your hotel. Savor a light lunch and take in the coastal views.",
            flight: { from: "Paris", to: "Faro", time: "08:00" },
            hotel: { name: "Lagos Bay Resort", nights: 4 },
            activities: [
                {
                    title: "Welcome Dinner",
                    description: "Enjoy a welcome dinner by the ocean and soak in the sunset...",
                    rating: "4.8/5",
                    vibe: "We love it!",
                    image: "/algarve.jpg"
                },
            ],
            foodRecommendations: [
                { title: "Fresh Seafood", description: "Taste the catch of the day." },
                { title: "Tropical Smoothie", description: "A refreshing blend of local fruits." }
            ]
        },
        {
            dayLabel: "Day 2",
            date: "2025-05-10",
            dayTitle: "Day 2: Beach and Local Culture",
            dayDescription: "Spend the day relaxing on the beach and exploring the local market. Immerse yourself in the vibrant local culture.",
            flight: null,
            hotel: { name: "Lagos Bay Resort", nights: 4 },
            activities: [
                {
                    title: "Welcome Dinner",
                    description: "Enjoy a welcome dinner by the ocean and soak in the sunset...",
                    rating: "4.8/5",
                    vibe: "We love it!",
                    image: "/algarve.jpg",
                    link: null
                },
                {
                    title: "Local Market",
                    description: "Discover unique local products and crafts...",
                    rating: "4.7/5",
                    vibe: "Vibrant",
                    image: "/algarve.jpg",
                    link: null
                }
            ],
            foodRecommendations: [
                { title: "Local Tapas", description: "Sample a variety of small dishes." },
                { title: "Icy Lemonade", description: "Perfect for a hot day." }
            ]
        }
    ],
    topActivities: [
        {
            title: "Ponta da Piedade",
            description: "Explore the stunning rock formations and crystal-clear waters...",
            rating: "4.5/5",
            vibe: "Relaxed",
            image: "/algarve.jpg",
            link: null
        },
        {
            title: "Welcome Dinner",
            description: "Enjoy a welcome dinner by the ocean and soak in the sunset...",
            rating: "4.8/5",
            vibe: "We love it!",
            image: "/algarve.jpg",
            link: null
        },
        {
            title: "Local Market",
            description: "Discover unique local products and crafts...",
            rating: "4.7/5",
            vibe: "Vibrant",
            image: "/algarve.jpg",
            link: null
        }
    ],
    flightBlockData: {
        outbound: {
            fromCity: "Paris",
            toCity: "Faro",
            departureTime: "08:00",
            duration: "2h40",
            airline: "Air Portugal",
            flightClass: "Economy",
            fromAirport: "Paris-Orly (ORY)",
            toAirport: "Faro (FAO)",
            baggage: "1 cabin bag + 1 checked bag included"
        },
        inbound: {
            fromCity: "Faro",
            toCity: "Paris",
            departureTime: "15:45",
            duration: "2h30",
            airline: "Air Portugal",
            flightClass: "Economy",
            fromAirport: "Faro (FAO)",
            toAirport: "Paris-Orly (ORY)",
            baggage: "1 cabin bag + 1 checked bag included"
        }
    },
    hotelData: {
        name: "Lagos Bay Resort",
        nights: 4,
        rating: 4.6,
        reviewsCount: 1352,
        location: "Lagos, Algarve, Portugal",
        amenities: ["Pool", "Spa", "Breakfast included", "Ocean view"],
        room: "Deluxe Suite with Balcony",
        website: "https://www.lagosbayresort.com",
        mapLink: "https://maps.google.com/search?q=Lagos+Bay+Resort"
    },
    messages: [
        { role: 'assistant', content: "Here’s a personalized trip to Algarve that I have planned for you." },
        { role: 'user', content: "The trip looks good! What’s the first day’s itinerary?" },
        { role: 'assistant', content: "On Day 1, you'll fly to Faro, check in at Lagos Bay Resort for 4 nights. You can relax at Ponta da Piedade, and try authentic cataplana." }
    ]
};

export default mockTripData;
