import { Route, Routes } from 'react-router-dom';
import Navigation from './Navigation';
import EvolutionTechnologique from './pages/EvolutionTechnologique';
import ThemeAstral from './pages/ThemeAstral';
// ...importe ici tes autres pages si besoin

export default function App() {
    return (
        <>
            <Navigation />
            <Routes>
                <Route path="/theme-astral" element={<ThemeAstral />} />
                <Route path="/evolution-technologique" element={<EvolutionTechnologique />} />
                {/* Ajoute ici d'autres routes, par exemple Accueil, Galerie, etc. */}
            </Routes>
        </>
    );
}



