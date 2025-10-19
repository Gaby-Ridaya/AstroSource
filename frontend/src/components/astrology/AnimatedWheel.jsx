
import React, { useEffect, useRef } from 'react';
import PlanetesOrbitsOverlay from './PlanetesOrbitsOverlay';

// Fonction utilitaire pour charger les scripts JS dans l'ordre
function loadScriptsInOrder(sources, onLoad) {
    let index = 0;
    function next() {
        if (index >= sources.length) {
            onLoad();
            return;
        }
        const script = document.createElement('script');
        script.src = sources[index];
        script.async = false;
        script.onload = () => {
            index++;
            next();
        };
        document.body.appendChild(script);
    }
    next();
}

export default function AnimatedWheel() {
    const canvasRef = useRef(null);

    const [angle, setAngle] = React.useState(0);
    const [themeData, setThemeData] = React.useState(null);

    // Charger theme_data.json pour avoir les couleurs des signes
    useEffect(() => {
        fetch('/data/theme_data.json')
            .then(response => response.json())
            .then(data => setThemeData(data))
            .catch(error => console.log('Couleurs signes non disponibles:', error));
    }, []);

    useEffect(() => {
        const scripts = [
            '/js/drawPlanetes.js',
            '/js/drawMaisons.js',
            '/js/drawAspects.js',
            '/js/drawWheel.js',
        ];
        loadScriptsInOrder(scripts, startAnimation);

        function startAnimation() {
            const canvas = canvasRef.current;
            if (!canvas || !window.drawWheelRotating) return;
            const ctx = canvas.getContext('2d');
            const planetNames = [
                'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn',
                'uranus', 'neptune', 'pluto', 'chiron', 'north-node', 'part-of-fortune'
            ];
            const signNames = [
                'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
                'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
            ];
            // Mapping images par nom
            const planetImages = {};
            planetNames.forEach(name => {
                const img = new window.Image();
                img.src = `/planetes_mini/${name}.png`;
                planetImages[name] = img;
            });
            const signImages = signNames.map(name => {
                const img = new window.Image();
                img.src = `/signes/${name}.png`;
                return img;
            });
            let loaded = 0;
            const total = planetNames.length + signImages.length;
            function checkLoaded() {
                loaded++;
                if (loaded === total) drawOnce();
            }
            // Charger toutes les images planètes et signes
            planetNames.forEach(name => {
                planetImages[name].onload = checkLoaded;
                planetImages[name].onerror = checkLoaded;
            });
            signImages.forEach(img => {
                img.onload = checkLoaded;
                img.onerror = checkLoaded;
            });
            function drawOnce() {
                // Nettoyage : on efface le fond explicitement pour éviter tout artefact
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.save();
                ctx.globalAlpha = 1;
                ctx.fillStyle = 'rgba(0,0,0,0)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.restore();
                // ATTENTION : Si un cercle ou texte rouge s'affiche encore, il est codé en dur dans drawWheelRotating.js
                // Il faut aller dans /public/js/drawWheelRotating.js (ou drawWheel.js) et supprimer tout code de debug (fillText, arc rouge, etc)
                window.drawWheelRotating(themeData, ctx, canvas, undefined, signImages, 0);
            }
        }
    // Nettoyage : rien à faire ici car les scripts restent globaux
    }, []);

    return (
        <div style={{ position: 'relative', width: 600, height: 600, margin: '0 auto' }}>
            {/* Halo visuel global sous la roue */}
            <div
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: 600,
                    height: 600,
                    borderRadius: '50%',
                    zIndex: 0,
                    pointerEvents: 'none',
                    boxShadow: '0 0 80px 32px rgba(0,246,255,0.10), 0 0 120px 60px rgba(0,153,168,0.07)'
                }}
            />
            <canvas ref={canvasRef} width={600} height={600} style={{ background: 'transparent', borderRadius: '50%', position: 'absolute', top: 0, left: 0, zIndex: 1, display: 'block' }} />
            {/* <CercleTurquoiseOverlay angle={0} /> */}
            <PlanetesOrbitsOverlay zIndex={5} />
        </div>
    );
}
