import React, { Suspense, lazy, useRef, useState } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import EtudeAstro from './components/EtudeAstro';
import './index.css';
import Navigation from './Navigation';
import Accueil from './pages/Accueil';
import EvolutionTechnologique from './pages/EvolutionTechnologique';
import Galerie from './pages/Galerie.jsx';
import ThemeAstral from './pages/ThemeAstral';
import VeritablePeintre from './pages/VeritablePeintre.jsx';


const YoutubeVideos = lazy(() => import('./pages/YoutubeVideos.jsx'));


function AudioProvider() {
    const audioRef = useRef(null);
    const [playing, setPlaying] = useState(false);

    const handleAudio = () => {
        if (!audioRef.current) return;
        if (playing) {
            audioRef.current.pause();
            setPlaying(false);
        } else {
            audioRef.current.play();
            setPlaying(true);
        }
    };

    return (
        <BrowserRouter>
            <Suspense fallback={<div style={{color:'#fff',textAlign:'center',marginTop:80}}>Chargement de la page vidéos...</div>}>
                <Routes>
                    <Route path="/" element={<Navigation audioRef={audioRef} playing={playing} handleAudio={handleAudio} />}>
                        <Route index element={<Accueil />} />
                        <Route path="theme-astral" element={<ThemeAstral />} />
                        <Route path="etude-astro" element={<EtudeAstro />} />
                        <Route path="galerie" element={<Galerie />} />
                        <Route path="veritable-peintre" element={<VeritablePeintre />} />
                        <Route path="evolution-technologique" element={<EvolutionTechnologique />} />
                        <Route path="videos" element={<YoutubeVideos />} />
                    </Route>
                </Routes>
            </Suspense>
            <audio ref={audioRef} src="/audio/astro_audio.mp3" loop preload="auto" />
        </BrowserRouter>
    );
}

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <AudioProvider />
    </React.StrictMode>
);
