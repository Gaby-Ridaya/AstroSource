import { Link } from 'react-router-dom';
import GalerieCategories from '../components/ui/GalerieCategories';

export default function Galerie() {
    return (
        <div style={{
            paddingTop: 60,
            width: '100vw',
            maxWidth: '100vw',
            overflowX: 'hidden',
        }}>
            <h1 style={{ color: '#00bcd4', textAlign: 'center', margin: '32px 0 24px', fontSize: '2.2em', fontWeight: 700, letterSpacing: 1.5 }}>
        Galerie AI
            </h1>
            <p style={{
                margin: '0 0 32px 0',
                color: '#e0f7fa',
                fontSize: '1.18em',
                textAlign: 'center',
                lineHeight: 1.7,
                fontFamily: 'Roboto, Arial, sans-serif',
                fontWeight: 400,
                letterSpacing: 0.2,
                width: '100%'
            }}>
        Toutes ces images ont été réalisées par l'interprétation de thèmes astrologiques. J'ai imaginé une IA astrologue qui pourrait aussi bien interpréter les thèmes astrologiques que créer une œuvre d'art avec les données astrologiques de la personne.
        Cette approche unique combine l'art de l'astrologie traditionnelle avec les possibilités créatives de l'intelligence artificielle. Chaque image générée reflète les énergies planétaires, les aspects astrologiques et les caractéristiques uniques du thème natal de chaque individu.
        L'IA analyse les positions des planètes, les maisons astrologiques, les signes du zodiaque et leurs interactions pour créer une représentation visuelle personnalisée. C'est une fusion fascinante entre la sagesse ancestrale de l'astrologie et la technologie moderne.
        Cette galerie présente donc des créations artistiques nées de l'interprétation de cartes du ciel, où chaque couleur, forme et symbole a une signification astrologique profonde.

        <br/><br/>
        🎨 <strong>Évolution Créative :</strong> Inspiré par Kerykeion pour la génération SVG des cartes du ciel, j'ai développé ma propre approche de visualisation astrologique.
        Les fichiers comme <code style={{ color: '#1de9ff', fontSize: '0.9em' }}>data/roue.svg/theme_2bc06bcc.svg</code> montrent cette évolution technique vers l'art génératif.
        <br/><br/>

        🤝 <strong>Appel à Collaboration :</strong> Je souhaite explorer avec d'autres développeurs créatifs de multiples modèles de cartes du ciel,
        différents formats de visualisation, et nouvelles approches artistiques. Ensemble, nous pourrions révolutionner l'art astrologique numérique !
        <br/><br/>

        🎵 <strong>Création Sonore :</strong> Découvrez "Astro Audio" - 29 minutes de composition musicale en Ré majeur (152 BPM),
        créée par analyse des harmonies astrologiques. Une symphonie des sphères où chaque note correspond aux énergies planétaires.
        <br/>
        <audio controls style={{ margin: '8px', width: '300px' }}>
            <source src="/audio/astro_audio.mp3" type="audio/mpeg" />
            Votre navigateur ne supporte pas l'audio.
        </audio>
        <br/>
        <small style={{ color: '#888', fontSize: '0.9em' }}>
            Qualité professionnelle • LUFS -14.26 dB • Analyse spectrale complète disponible
        </small>
        <br/><br/>

        Dans l'onglet <Link to="/veritable-peintre" style={{ color: '#1de9ff', textDecoration: 'underline', fontWeight: 600, cursor: 'pointer' }}>Véritable Peintres</Link>, vous pouvez découvrir d'autres créations artistiques...
            </p>
            <GalerieCategories />
        </div>
    );
}
