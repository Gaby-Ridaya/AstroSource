import { Link, Outlet } from 'react-router-dom';

export default function Navigation({ audioRef, playing, handleAudio }) {
    return (
        <>
            <nav style={{
                background: 'linear-gradient(90deg, #0a0a23 80%, #18184a 100%)',
                padding: '10px 20px',
                display: 'flex',
                gap: 20,
                alignItems: 'center',
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100vw',
                zIndex: 1000,
                boxShadow: 'none'
            }}>
                <style>{`
          @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap');
          .nav-link {
            color: #00bcd4;
            text-decoration: none;
            font-size: 1.18em;
            font-family: 'Orbitron', Arial, sans-serif;
            font-weight: 600;
            letter-spacing: 1.5px;
            text-shadow: 0 2px 8px #0ff3, 0 1px 2px #000a;
            transition: color 0.2s, text-shadow 0.2s;
          }
          .nav-link:hover {
            color: #1de9ff;
            text-shadow: 0 2px 16px #1de9ff99, 0 1px 2px #000a;
          }
          .audio-btn {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            border: none;
            background: radial-gradient(circle at 60% 40%, #1de9ff 60%, #00bcd4 100%, #18184a 120%);
            box-shadow: 0 0 16px #1de9ff99, 0 0 8px #00bcd4cc;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: 18px;
            cursor: pointer;
            transition: box-shadow 0.2s, background 0.2s;
            outline: none;
          }
          .audio-btn:hover {
            box-shadow: 0 0 32px #1de9ffcc, 0 0 16px #00bcd4cc;
            background: radial-gradient(circle at 60% 40%, #1de9ff 80%, #00bcd4 100%, #18184a 120%);
          }
          .audio-btn img {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            object-fit: cover;
            box-shadow: 0 0 8px 2px #1de9ff88, 0 0 16px 4px #00bcd488;
            filter: brightness(1.15) saturate(1.2);
            background: transparent;
            transition: box-shadow 0.2s, filter 0.2s;
          }
          .audio-btn:hover img {
            box-shadow: 0 0 16px 6px #1de9ffbb, 0 0 24px 8px #00bcd4aa;
            filter: brightness(1.25) saturate(1.3);
          }
        `}</style>
                <Link className="nav-link" to="/">Accueil</Link>
                <Link className="nav-link" to="/theme-astral">Thème Astral</Link>
                <Link className="nav-link" to="/etude-astro">Étude Astro</Link>
                <Link className="nav-link" to="/galerie">Galerie AI</Link>
                <Link className="nav-link" to="/veritable-peintre">Véritable Peintres</Link>
                <Link className="nav-link" to="/evolution-technologique">Évolution Tech</Link>
                <Link className="nav-link" to="/videos">Vidéos</Link>
                <div style={{ flex: 1 }} />
                <button className="audio-btn" onClick={handleAudio} title={playing ? 'Arrêter la musique' : 'Jouer la musique'} style={{ marginRight: 32 }}>
                    <img src="/roue/rose_astro.png" alt="Musique astrologique" />
                </button>
            </nav>
            <div style={{ height: 60, background: 'transparent', border: 'none', boxShadow: 'none' }} />
            <Outlet />
        </>
    );
}
