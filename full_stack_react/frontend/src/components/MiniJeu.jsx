// MiniJeu.js
import React, { useRef, useEffect, useState } from 'react';

const canvasWidth = 400;
const canvasHeight = 600;
const playerWidth = 40;
const playerHeight = 40;
const playerSpeed = 5;
const obstacleWidth = 50;
const obstacleHeight = 20;
const obstacleSpeed = 2;

const MiniJeu = () => {
    const canvasRef = useRef(null);
    const [playerX, setPlayerX] = useState(canvasWidth / 2 - playerWidth / 2);
    const [obstacles, setObstacles] = useState([]);
    const [gameOver, setGameOver] = useState(false);

    // Fonction pour dessiner l'avion
    const drawPlayer = (ctx, x, y) => {
        ctx.fillStyle = 'blue';
        // On peut dessiner l'avion sous forme de triangle ou rectangle. Ici, nous utilisons un triangle pour un effet "avion"
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + playerWidth, y);
        ctx.lineTo(x + playerWidth / 2, y - playerHeight);
        ctx.closePath();
        ctx.fill();
    };

    // Fonction pour dessiner les obstacles
    const drawObstacle = (ctx, obstacle) => {
        ctx.fillStyle = 'red';
        ctx.fillRect(obstacle.x, obstacle.y, obstacleWidth, obstacleHeight);
    };

    // Mise à jour de la position de l’avion via les touches fléchées
    const handleKeyDown = (e) => {
        if (e.key === 'ArrowLeft') {
            setPlayerX(prev => Math.max(prev - playerSpeed, 0));
        } else if (e.key === 'ArrowRight') {
            setPlayerX(prev => Math.min(prev + playerSpeed, canvasWidth - playerWidth));
        }
    };

    // Vérification de la collision entre l'avion et un obstacle
    const checkCollision = (playerX, obstacle) => {
        const playerY = canvasHeight - 20; // Position verticale fixe de l'avion
        if (
            playerX < obstacle.x + obstacleWidth &&
            playerX + playerWidth > obstacle.x &&
            playerY - playerHeight < obstacle.y + obstacleHeight &&
            playerY > obstacle.y
        ) {
            return true;
        }
        return false;
    };

    // Boucle d'animation et mise à jour du canvas
    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        let animationFrameId;
        let lastObstacleTime = 0;

        const render = (timestamp) => {
            // Effacer le canvas
            ctx.clearRect(0, 0, canvasWidth, canvasHeight);

            // Dessiner le fond (par exemple des nuages ou un dégradé)
            ctx.fillStyle = '#e0f7fa';
            ctx.fillRect(0, 0, canvasWidth, canvasHeight);

            // Dessiner l'avion à la position calculée
            const playerY = canvasHeight - 20; // position fixe en bas du canvas
            drawPlayer(ctx, playerX, playerY);

            // Générer de nouveaux obstacles toutes les 2 secondes (modifiable)
            if (timestamp - lastObstacleTime > 2000) {
                const obstacleX = Math.random() * (canvasWidth - obstacleWidth);
                setObstacles(prev => [...prev, { x: obstacleX, y: -obstacleHeight }]);
                lastObstacleTime = timestamp;
            }

            // Mise à jour et affichage des obstacles
            setObstacles(prevObstacles =>
                prevObstacles.map(obstacle => ({ ...obstacle, y: obstacle.y + obstacleSpeed }))
            );

            obstacles.forEach(obstacle => {
                drawObstacle(ctx, obstacle);
                // Vérification des collisions
                if (checkCollision(playerX, playerY, obstacle)) {
                    setGameOver(true);
                }
            });

            // Retirer les obstacles qui sortent du canvas
            setObstacles(prevObstacles =>
                prevObstacles.filter(obstacle => obstacle.y < canvasHeight)
            );

            if (!gameOver) {
                animationFrameId = requestAnimationFrame(render);
            } else {
                // Afficher un message game over
                ctx.fillStyle = 'black';
                ctx.font = '30px Arial';
                ctx.fillText('Game Over', canvasWidth / 2 - 70, canvasHeight / 2);
            }
        };

        animationFrameId = requestAnimationFrame(render);
        return () => {
            cancelAnimationFrame(animationFrameId);
        };
    }, [playerX, obstacles, gameOver]);

    // Ajout des écouteurs d'événements pour la gestion du clavier
    useEffect(() => {
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, []);

    return (
        <div style={{ textAlign: 'center' }}>
            <canvas ref={canvasRef} width={canvasWidth} height={canvasHeight} style={{ border: '1px solid #000' }} />
            {gameOver && <p>Recommencez en rechargeant la page ou en déclenchant un reset !</p>}
        </div>
    );
};

export default MiniJeu;
