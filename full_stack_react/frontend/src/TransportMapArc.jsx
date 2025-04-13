import React, {
    useRef,
    useState,
    useEffect,
    useMemo
} from "react";
import {
    ComposableMap,
    Geographies,
    Geography,
    Marker
} from "react-simple-maps";
import { geoMercator } from "d3-geo";
import { useMotionValue, animate } from "framer-motion";

// --------------- Données ---------------
const fromCoords = [2.3522, 48.8566]; // Paris
const toCoords = [-7.935, 37.0179];   // Faro

const features = {
    type: "FeatureCollection",
    features: [
        {
            type: "Feature",
            geometry: {
                type: "MultiPoint",
                coordinates: [fromCoords, toCoords]
            }
        }
    ]
};

// --------------- Hook local de resize ---------------
function useContainerSize(ref) {
    const [size, setSize] = useState({ width: 0, height: 0 });

    useEffect(() => {
        if (!ref.current) return;

        const handleResize = (entries) => {
            if (!entries || entries.length === 0) return;
            const { width, height } = entries[0].contentRect;
            setSize({ width, height });
        };

        // Création d'un ResizeObserver natif
        const observer = new ResizeObserver(handleResize);
        observer.observe(ref.current);

        return () => {
            observer.disconnect();
        };
    }, [ref]);

    return size;
}

// --------------- Fonctions Bézier lat/lng ---------------
function getControlPointLatLng(from, to, factor = 0.3) {
    const [lon1, lat1] = from;
    const [lon2, lat2] = to;
    const mid = [(lon1 + lon2) / 2, (lat1 + lat2) / 2];
    const dx = lon2 - lon1;
    const dy = lat2 - lat1;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const offset = factor * dist;
    const perp = [-dy, dx];
    const norm = Math.sqrt(perp[0] * perp[0] + perp[1] * perp[1]);
    const offsetVec = [(perp[0] / norm) * offset, (perp[1] / norm) * offset];
    return [mid[0] + offsetVec[0], mid[1] + offsetVec[1]];
}

function getQuadLatLng(t, from, control, to) {
    const lon =
        (1 - t) ** 2 * from[0] +
        2 * (1 - t) * t * control[0] +
        t ** 2 * to[0];
    const lat =
        (1 - t) ** 2 * from[1] +
        2 * (1 - t) * t * control[1] +
        t ** 2 * to[1];
    return [lon, lat];
}

function buildArcPath(projection, from, to, factor = 0.3, n = 30) {
    const control = getControlPointLatLng(from, to, factor);
    let path = "";
    for (let i = 0; i <= n; i++) {
        const t = i / n;
        const [lon, lat] = getQuadLatLng(t, from, control, to);
        const [x, y] = projection([lon, lat]);
        if (i === 0) {
            path += `M ${x},${y}`;
        } else {
            path += ` L ${x},${y}`;
        }
    }
    return path;
}

// --------------- Composant ---------------
export default function TravelMapResponsive() {
    const containerRef = useRef(null);

    // On récupère la taille courante du conteneur (width, height)
    const size = useContainerSize(containerRef);

    // Projection & arcPath
    const projection = useMemo(() => {
        // Si pas encore de taille, renvoie une projection par défaut
        if (size.width < 2 || size.height < 2) {
            return geoMercator();
        }
        // fitSize => zoom auto sur Paris/Faro
        const proj = geoMercator();
        proj.fitSize([size.width, size.height], features);
        return proj;
    }, [size]);

    const [arcPath, setArcPath] = useState("");

    useEffect(() => {
        if (size.width < 2 || size.height < 2) {
            setArcPath("");
            return;
        }
        // On calcule l'arc en pixels
        const path = buildArcPath(projection, fromCoords, toCoords, 0.3, 30);
        setArcPath(path);
    }, [projection, size]);

    // Avion animé
    const progress = useMotionValue(0);

    useEffect(() => {
        const controls = animate(progress, 1, { duration: 4, delay: 1, ease: "linear" });
        return () => controls.stop();
    }, [progress]);

    const [planeLatLng, setPlaneLatLng] = useState(fromCoords);
    useEffect(() => {
        const unsub = progress.onChange((val) => {
            const ctrl = getControlPointLatLng(fromCoords, toCoords, 0.3);
            const newPos = getQuadLatLng(val, fromCoords, ctrl, toCoords);
            setPlaneLatLng(newPos);
        });
        return () => unsub();
    }, []);

    return (
        <div
            ref={containerRef}
            style={{
                width: "100%",
                height: "100%",
                border: "1px solid #ccc",
                boxSizing: "border-box"
            }}
        >
            {/* On attend que size soit établi pour afficher la carte */}
            {size.width > 0 && size.height > 0 && (
                <ComposableMap
                    projection={projection}
                    // On n'indique pas width/height fixes, 
                    // on laisse la carte prendre 100% du conteneur
                    style={{ width: "100%", height: "100%" }}
                >
                    <Geographies geography="https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json">
                        {({ geographies }) =>
                            geographies.map((geo) => (
                                <Geography
                                    key={geo.rsmKey}
                                    geography={geo}
                                    fill="#dddddd"
                                    stroke="#999999"
                                />
                            ))
                        }
                    </Geographies>

                    {/* Arc */}
                    {arcPath && (
                        <path
                            d={arcPath}
                            fill="none"
                            stroke="grey"
                            strokeWidth={2}
                            strokeLinecap="round"
                        />
                    )}

                    {/* Markers lat/lng : Paris & Faro */}
                    <Marker coordinates={fromCoords}>
                        <circle r={3} fill="#F53" />
                        <text
                            y={-10}
                            textAnchor="middle"
                            style={{ fontSize: "10px", fill: "#333" }}
                        >
                            Paris
                        </text>
                    </Marker>

                    <Marker coordinates={toCoords}>
                        <circle r={3} fill="#F53" />
                        <text
                            y={-10}
                            textAnchor="middle"
                            style={{ fontSize: "10px", fill: "#333" }}
                        >
                            Faro
                        </text>
                    </Marker>

                    {/* Avion animé en lat/lng */}
                    <Marker coordinates={planeLatLng}>
                        <text
                            textAnchor="middle"
                            y={-10}
                            style={{ fontSize: "20px", fill: "#000" }}
                        >
                            ✈️
                        </text>
                    </Marker>
                </ComposableMap>
            )}
        </div>
    );
}
