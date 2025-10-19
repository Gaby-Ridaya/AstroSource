import { useEffect, useState } from 'react';
import { apiService } from '../services/apiService';
import './EtudeAstro.css';

function EtudeAstro() {
    const [interpretations, setInterpretations] = useState({
        planets: {},
        houses: {}
    });
    const [celebrities, setCelebrities] = useState([]);
    const [selectedInterpretation, setSelectedInterpretation] = useState(null);
    const [selectedCelebrity, setSelectedCelebrity] = useState(null);
    const [activeTab, setActiveTab] = useState('planets');
    const [loading, setLoading] = useState(true);

    // Charger les données depuis l'API
    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            try {
                const [planetsData, housesData, celebritiesData] = await Promise.all([
                    apiService.getPlanetsInterpretations(),
                    apiService.getHousesInterpretations(),
                    apiService.getCelebrities()
                ]);

                setInterpretations({ planets: planetsData, houses: housesData });
                setCelebrities(celebritiesData);
            } catch (error) {
                console.error('Erreur lors du chargement des données:', error);
                setError('Erreur lors du chargement des données astreologiques');
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, []);    // Charger la liste des célébrités
    useEffect(() => {
        const loadCelebrities = async () => {
            try {
                const response = await fetch('/api/celebrities');
                const data = await response.json();
                setCelebrities(data);
            } catch (error) {
                console.error('Erreur lors du chargement des célébrités:', error);
            }
        };

        loadCelebrities();
    }, []);

    // Fonction pour organiser les interprétations par planète/signe
    const organizeInterpretations = (data) => {
        const organized = {};

        Object.keys(data).forEach(key => {
            const parts = key.split('_');
            if (parts.length >= 3) {
                const planet = parts[0];
                const type = parts[1]; // 'maison' ou signe
                const location = parts[2];

                if (!organized[planet]) {
                    organized[planet] = {};
                }
                if (!organized[planet][type]) {
                    organized[planet][type] = {};
                }
                organized[planet][type][location] = data[key];
            }
        });

        return organized;
    };

    const organizedData = activeTab === 'planets'
        ? organizeInterpretations(interpretations.planets)
        : organizeInterpretations(interpretations.houses);

    // Fonction pour ouvrir une interprétation
    const openInterpretation = (planet, type, location, content) => {
        setSelectedInterpretation({
            title: `${planet} en ${type} ${location}`,
            content
        });
    };

    // Fonction pour ouvrir un thème de célébrité
    const openCelebrity = (celebrity) => {
        setSelectedCelebrity(celebrity);
    };

    if (loading) {
        return (
            <div className="etude-astro">
                <div className="loading">
                    <h2>🔮 Chargement des données astrologiques...</h2>
                </div>
            </div>
        );
    }

    return (
        <div className="etude-astro">
            {/* Header */}
            <div className="etude-header">
                <h1>📚 Étude Astrologique</h1>
                <p>Explorez les interprétations astrologiques et les thèmes de célébrités</p>
            </div>

            {/* Navigation */}
            <div className="etude-nav">
                <button
                    className={activeTab === 'planets' ? 'active' : ''}
                    onClick={() => setActiveTab('planets')}
                >
                    🪐 Planètes
                </button>
                <button
                    className={activeTab === 'houses' ? 'active' : ''}
                    onClick={() => setActiveTab('houses')}
                >
                    🏠 Maisons
                </button>
            </div>

            <div className="etude-content">
                {/* Panneau des interprétations à gauche */}
                <div className="interpretations-panel">
                    <h3>📖 Interprétations</h3>
                    <div className="interpretations-list">
                        {Object.keys(organizedData).map(planet => (
                            <div key={planet} className="planet-section">
                                <h4 className="planet-title">{planet}</h4>
                                {Object.keys(organizedData[planet]).map(type => (
                                    <div key={type} className="type-section">
                                        <h5 className="type-title">{type}</h5>
                                        {Object.keys(organizedData[planet][type]).map(location => (
                                            <button
                                                key={location}
                                                className="interpretation-item"
                                                onClick={() => openInterpretation(
                                                    planet,
                                                    type,
                                                    location,
                                                    organizedData[planet][type][location]
                                                )}
                                            >
                                                {planet} en {type} {location}
                                            </button>
                                        ))}
                                    </div>
                                ))}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Panneau central - Contenu sélectionné */}
                <div className="content-panel">
                    {selectedInterpretation ? (
                        <div className="interpretation-display">
                            <div className="interpretation-header">
                                <h3>{selectedInterpretation.title}</h3>
                                <button
                                    className="close-btn"
                                    onClick={() => setSelectedInterpretation(null)}
                                >
                                    ✕
                                </button>
                            </div>
                            <div className="interpretation-content">
                                {selectedInterpretation.content.split('\n').map((paragraph, index) => (
                                    <p key={index}>{paragraph}</p>
                                ))}
                            </div>
                        </div>
                    ) : selectedCelebrity ? (
                        <div className="celebrity-display">
                            <div className="celebrity-header">
                                <h3>⭐ {selectedCelebrity.name}</h3>
                                <button
                                    className="close-btn"
                                    onClick={() => setSelectedCelebrity(null)}
                                >
                                    ✕
                                </button>
                            </div>
                            <div className="celebrity-chart">
                                <img
                                    src={selectedCelebrity.svgPath}
                                    alt={`Thème astral de ${selectedCelebrity.name}`}
                                    className="celebrity-svg"
                                />
                            </div>
                        </div>
                    ) : (
                        <div className="welcome-message">
                            <h3>🌟 Bienvenue dans l'Étude Astrologique</h3>
                            <p>Sélectionnez une interprétation à gauche ou un thème de célébrité à droite pour commencer votre étude.</p>
                        </div>
                    )}
                </div>

                {/* Panneau des célébrités à droite */}
                <div className="celebrities-panel">
                    <h3>⭐ Thèmes de Célébrités</h3>
                    <div className="celebrities-list">
                        {celebrities.map((celebrity, index) => (
                            <button
                                key={index}
                                className="celebrity-item"
                                onClick={() => openCelebrity(celebrity)}
                            >
                                <div className="celebrity-avatar">⭐</div>
                                <span className="celebrity-name">{celebrity.name}</span>
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* Modal pour les interprétations (version mobile) */}
            {selectedInterpretation && (
                <div className="modal-overlay" onClick={() => setSelectedInterpretation(null)}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>{selectedInterpretation.title}</h3>
                            <button
                                className="close-btn"
                                onClick={() => setSelectedInterpretation(null)}
                            >
                                ✕
                            </button>
                        </div>
                        <div className="modal-body">
                            {selectedInterpretation.content.split('\n').map((paragraph, index) => (
                                <p key={index}>{paragraph}</p>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default EtudeAstro;
