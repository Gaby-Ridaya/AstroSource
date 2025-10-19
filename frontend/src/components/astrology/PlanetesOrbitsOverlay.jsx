// Copyright (c) 2023-2025 Gaby. Tous droits réservés.
// Ce fichier fait partie du projet AstroSource. Toute reproduction ou utilisation non autorisée est interdite.
import React, { useEffect, useRef } from 'react';

// Tableau des planètes avec rayon et vitesse (ordre : lune rapide, pluton lent)
const PLANETES = [
    { name: 'moon', label: 'Lune', color: '#fff', radius: 70, speed: 0.06 }, // la plus rapide
    { name: 'mercury', label: 'Mercure', color: '#b0c4de', radius: 90, speed: 0.045 },
    { name: 'venus', label: 'Vénus', color: '#f8bbd0', radius: 110, speed: 0.032 },
    { name: 'sun', label: 'Soleil', color: '#ffe066', radius: 130, speed: 0.027 },
    { name: 'mars', label: 'Mars', color: '#ff5252', radius: 150, speed: 0.022 },
    { name: 'jupiter', label: 'Jupiter', color: '#ffd700', radius: 170, speed: 0.014 },
    { name: 'saturn', label: 'Saturne', color: '#bdbdbd', radius: 190, speed: 0.011 },
    { name: 'uranus', label: 'Uranus', color: '#00e5ff', radius: 210, speed: 0.008 },
    { name: 'neptune', label: 'Neptune', color: '#2979ff', radius: 230, speed: 0.006 },
    { name: 'pluto', label: 'Pluton', color: '#b39ddb', radius: 250, speed: 0.003 }, // la plus lente
    { name: 'chiron', label: 'Chiron', color: '#e57373', radius: 270, speed: 0.004 },
    { name: 'north-node', label: 'Noeud Nord', color: '#fff', radius: 210, speed: 0.005 },
    { name: 'part-of-fortune', label: 'Part de Fortune', color: '#fffde7', radius: 230, speed: 0.0045 },
];

export default function PlanetesOrbitsOverlay({ zIndex = 10, style = {} }) {
    const canvasRef = useRef(null);
    const anglesRef = useRef(PLANETES.map(() => 0));

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        let animationId;

        // Précharge les images
        const images = {};
        PLANETES.forEach(p => {
            const img = new window.Image();
            img.src = `/planetes_mini/${p.name}.png`;
            images[p.name] = img;
        });

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            // Répartit chaque planète à une position différente sur son cercle (360°/13)
            const total = PLANETES.length;
            PLANETES.forEach((p, i) => {
                const angle = anglesRef.current[i];
                ctx.save();
                ctx.translate(cx, cy);
                ctx.rotate(angle);
                // Cercles d'orbite rendus totalement invisibles
                // Fixe la planète à une position unique sur son cercle
                const planetAngle = (2 * Math.PI * i) / total;
                const x = p.radius * Math.cos(planetAngle);
                const y = p.radius * Math.sin(planetAngle);
                ctx.save();
                ctx.translate(x, y);
                ctx.rotate(planetAngle + Math.PI / 2);
                const img = images[p.name];
                if (img && img.complete && img.naturalWidth > 0) {
                    ctx.beginPath();
                    ctx.arc(0, 0, 18, 0, 2 * Math.PI);
                    ctx.clip();
                    ctx.drawImage(img, -18, -18, 36, 36);
                } else {
                    ctx.beginPath();
                    ctx.arc(0, 0, 18, 0, 2 * Math.PI);
                    ctx.fillStyle = p.color;
                    ctx.globalAlpha = 1.0;
                    ctx.fill();
                }
                ctx.restore();
                ctx.restore();
            });
        }

        function animate() {
            // Avance chaque angle selon la vitesse de la planète
            PLANETES.forEach((p, i) => {
                anglesRef.current[i] += p.speed;
                if (anglesRef.current[i] > Math.PI * 2) anglesRef.current[i] -= Math.PI * 2;
            });
            draw();
            animationId = requestAnimationFrame(animate);
        }
        animate();
        return () => cancelAnimationFrame(animationId);
    }, []);

    return (
        <canvas
            ref={canvasRef}
            width={600}
            height={600}
            style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: 600,
                height: 600,
                margin: '0 auto',
                display: 'block',
                pointerEvents: 'none',
                background: 'transparent',
                borderRadius: '50%',
                zIndex,
                ...style,
            }}
        />
    );
}
