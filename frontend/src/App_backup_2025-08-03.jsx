import { useState } from 'react';
import './App.css';
import UserFilesList from './components/UserFilesList';
import { apiService } from './services/apiService';

export default function App() {
    const [nom, setNom] = useState('');
    const [ville, setVille] = useState('');
    const [date, setDate] = useState('');
    const [heure, setHeure] = useState('');
    const [svgContent, setSvgContent] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            console.log('Envoi des données:', { nom, ville_naissance: ville, date_naissance: date, heure_naissance: heure });

            const data = await apiService.generateTheme({
                nom: nom,
                ville_naissance: ville,
                date_naissance: date,
                heure_naissance: heure
            });

            console.log('Réponse reçue:', data);

            if (data.svg_content) {
                let svgData = data.svg_content;
                svgData = svgData.replace(/data-timestamp="[^"]*"/g, '');

                if (!svgData.includes('viewBox')) {
                    svgData = svgData.replace('<svg', '<svg viewBox="0 0 1800 1200"');
                }

                console.log('SVG avec couleurs préservées:', svgData.substring(0, 500));
                setSvgContent(svgData);
                console.log('SVG intégré directement avec couleurs préservées');
            } else {
                setError('Pas de contenu SVG reçu');
            }
        } catch (err) {
            console.error('Erreur:', err);
            setError('Erreur: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <div className="main-content">
                <div className="left-panel">
                    <h1>� Générateur de Thème Astral</h1>
                    <form onSubmit={handleSubmit}>
                        <div>
                            <label>Nom:</label>
                            <input
                                type="text"
                                value={nom}
                                onChange={(e) => setNom(e.target.value)}
                                required
                                placeholder="Votre nom"
                            />
                        </div>
                        <div>
                            <label>Ville de naissance:</label>
                            <input
                                type="text"
                                value={ville}
                                onChange={(e) => setVille(e.target.value)}
                                required
                                placeholder="Paris, France"
                            />
                        </div>
                        <div>
                            <label>Date de naissance:</label>
                            <input
                                type="date"
                                value={date}
                                onChange={(e) => setDate(e.target.value)}
                                required
                            />
                        </div>
                        <div>
                            <label>Heure de naissance:</label>
                            <input
                                type="time"
                                value={heure}
                                onChange={(e) => setHeure(e.target.value)}
                                required
                            />
                        </div>
                        <button type="submit" disabled={loading}>
                            {loading ? 'GÉNÉRATION...' : 'GÉNÉRER MON THÈME'}
                        </button>
                    </form>
                    {error && <div style={{color: 'red'}}>{error}</div>}
                    {/* Affichage des fichiers générés pour l'utilisateur */}
                    <div style={{marginTop:32}}>
                        <UserFilesList user={nom} />
                    </div>
                </div>
                <div className="right-panel">
                    {svgContent ? (
                        <div>
                            <h3>🎨 VOTRE CARTE DU CIEL</h3>
                            <div className="svg-display" style={{
                                width: '100%',
                                height: 'auto',
                                maxHeight: '700px',
                                background: 'white',
                                borderRadius: '8px',
                                overflow: 'auto',
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center'
                            }}>
                                <div
                                    dangerouslySetInnerHTML={{ __html: svgContent }}
                                    style={{
                                        width: '100%',
                                        height: 'auto',
                                        maxWidth: '100%'
                                    }}
                                />
                            </div>
                        </div>
                    ) : (
                        <div>
                            <h3>🌙 En attente...</h3>
                            <p>Remplissez le formulaire pour voir votre thème astral</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
