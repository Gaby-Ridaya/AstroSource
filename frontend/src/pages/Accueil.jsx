import { Suspense, lazy, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/accueil.css';

// Import lazy avec gestion d'erreur
const AnimatedWheel = lazy(() =>
    import('../components/astrology/AnimatedWheel').catch(() => ({
        default: () => <SimpleWheel />
    }))
);

const NB_ETOILES = 120;

export function SuperEtoiles() {
    useEffect(() => {
        const container = document.getElementById('etoiles');
        if (!container) return;
        container.innerHTML = '';
        for (let i = 0; i < NB_ETOILES; i++) {
            const star = document.createElement('div');
            star.className = 'etoile';
            star.style.top = `${Math.random() * 100  }%`;
            star.style.left = `${Math.random() * 100  }%`;
            star.style.animationDuration = `${1 + Math.random() * 2.5  }s`;
            star.style.filter = `blur(${Math.random() * 1.5}px)`;
            container.appendChild(star);
        }
    }, []);
    return <div className="etoiles" id="etoiles"></div>;
}

// Composant de remplacement temporaire pour AnimatedWheel
function SimpleWheel() {
    return (
        <div style={{
            width: 400,
            height: 400,
            borderRadius: '50%',
            border: '3px solid #7fdfff',
            background: 'radial-gradient(circle, rgba(127,223,255,0.1) 0%, rgba(127,223,255,0.05) 50%, transparent 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            animation: 'rotate 30s linear infinite',
            boxShadow: '0 0 30px rgba(127,223,255,0.3)',
        }}>
            <div style={{
                color: '#7fdfff',
                fontSize: '18px',
                fontWeight: 'bold',
                textAlign: 'center',
                textShadow: '0 2px 10px rgba(0,0,0,0.5)'
            }}>
                🌟<br/>
                Roue Astrale<br/>
                ✨
            </div>
            <style>{`
                @keyframes rotate {
                    from { transform: rotate(0deg); }
                    to { transform: rotate(360deg); }
                }
            `}</style>
        </div>
    );
}


function Accueil() {
    const [hover, setHover] = useState(false);
    const navigate = useNavigate();

    return (
        <>
            <SuperEtoiles />
            <div style={{
                display: 'flex',
                flexDirection: 'row',
                alignItems: 'flex-start',
                width: '100%',
                marginTop: 60,
                marginBottom: 40,
                position: 'relative',
                zIndex: 2,
            }}>
                <div style={{ minWidth: 420, maxWidth: 420, height: 420, display: 'flex', alignItems: 'center', justifyContent: 'flex-start', marginLeft: 40 }}>
                    <Suspense fallback={<SimpleWheel />}>
                        <AnimatedWheel />
                    </Suspense>
                </div>
            </div>
            <div style={{
                position: 'fixed',
                top: '50%',
                right: '8vw',
                transform: 'translateY(-50%)',
                maxWidth: 540,
                minWidth: 340,
                width: '36vw',
                color: '#fff',
                fontFamily: 'Georgia, serif',
                fontSize: '1em',
                lineHeight: 1.5,
                textShadow: '0 2px 16px #000a',
                padding: '32px 32px',
                zIndex: 10,
                borderRadius: '24px',
                pointerEvents: 'none',
                boxSizing: 'border-box',
                background: 'none',
                boxShadow: 'none',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'flex-start',
                justifyContent: 'center',
                textAlign: 'left',
                overflow: 'visible',
            }}>
                <div style={{pointerEvents: 'auto', width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'flex-start', justifyContent: 'flex-start'}}>
                    <p style={{fontWeight:'bold',fontSize:'1em',color:'#7fdfff', marginBottom: '0.2em', marginTop: 0, lineHeight: 1.5}}>Vous avez vu votre thème.<br/>Mais avez-vous déjà vu votre image astrale&nbsp;?</p>
                    <p style={{margin: 0, fontSize:'1em', color:'#7fdfff', lineHeight: 1.5}}>À partir de vos données de naissance, exactement comme pour un thème astrologique, notre générateur compose votre image astrale personnalisée.</p>
                    <p style={{margin: 0, fontSize:'1em', color:'#7fdfff', lineHeight: 1.5}}>Vous recevez également votre roue astrologique, accompagnée d’interprétations poétiques.</p>
                    <p style={{color:'#7fdfff',fontWeight:'bold', fontSize:'1em', margin: 0, lineHeight: 1.5}}>Mais sa fonction première est toute autre&nbsp;:<br/>
                        <span style={{color:'#7fdfff',fontWeight:'normal'}}>Faire apparaître votre empreinte céleste sous forme d’image — magique, évocatrice, mystérieuse.</span>
                    </p>
                    <p style={{fontSize:'1em', color:'#7fdfff', margin: 0, lineHeight: 1.5}}>
            Une œuvre.<br/>Un talisman.<br/>
            Quelque chose que vous n’avez jamais vu de vous-même.
                    </p>
                    <p style={{fontSize:'1em', color:'#7fdfff', margin: 0, lineHeight: 1.5}}>Une fois créée, vous pouvez l'imprimer, la contempler. Vous pouvez aussi créer des images pour vos proches, un cadeau unique, mysthique et magique.</p>
                    <p style={{margin: 0, fontSize:'1em', color:'#7fdfff', lineHeight: 1.5}}>Ce que vous recevez, ce n’est pas un simple thème&nbsp;:</p>
                    <div style={{margin:'0.7em 0 0.7em 1.2em',color:'#7fdfff',fontStyle:'italic',fontSize:'1em', lineHeight: 1.5}}>
                        <div>C’est votre reflet astral.<br/>L’image de ce qui vous habite.</div>
                    </div>
                    <p style={{color:'#a259e6',fontWeight:'bold',fontSize:'1em', margin: 0, lineHeight: 1.5}}>Découvrez ce que votre ciel révèle… quand il devient une œuvre.</p>
                    <button
                        style={{
                            marginTop: 24,
                            background: '#4fc3ff',
                            color: '#fff',
                            border: 'none',
                            borderRadius: 20,
                            padding: '12px 32px',
                            fontSize: '1em',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                            boxShadow: hover ? '0 0 24px 6px #7fdfff, 0 2px 12px #0003' : '0 2px 12px #0003',
                            transition: 'box-shadow 0.2s, background 0.2s',
                            outline: 'none',
                            letterSpacing: '0.01em',
                        }}
                        onMouseEnter={() => setHover(true)}
                        onMouseLeave={() => setHover(false)}
                        onClick={() => navigate('/theme-astral')}
                    >
            Générez votre image Astrale
                    </button>
                </div>
            </div>
        </>
    );
}

export default Accueil;


