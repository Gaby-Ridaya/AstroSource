import React from 'react';

export default function VeritablePeintre() {
    return (
        <div style={{ paddingTop: 60, color: '#e0f7fa', minHeight: '80vh', textAlign: 'center', width: '100vw', maxWidth: '100vw', overflowX: 'hidden' }}>
            <h1 style={{ color: '#00bcd4', margin: '32px 0 24px', fontSize: '2.2em', fontWeight: 700, letterSpacing: 1.5 }}>
        Véritable Peintres
            </h1>
            <p style={{ fontSize: '1.18em', width: '100%', margin: '0 0 32px 0', lineHeight: 1.7 }}>
                <span style={{ color: '#1de9ff', fontWeight: 700, fontSize: '1.22em' }}>Véritables peintres, vraies œuvres</span><br />
        Regarde ces collections vidéo de maîtres intemporels<br /><br />
        Ici, vous pouvez comparer les œuvres générées par l’IA avec celles des véritables peintres. <br />
        Cette page met en avant l’authenticité, la technique et l’âme des grands maîtres de l’histoire de l’art.<br /><br />
        Clique ici pour découvrir les œuvres des grands maîtres.<br /><br />
                <a href="https://www.youtube.com/@ruzhili" target="_blank" rel="noopener noreferrer" style={{ color: '#1de9ff', fontWeight: 600, textDecoration: 'underline', display: 'inline-block', marginBottom: 8 }}>
          Chaîne YouTube de véritables peintres
                </a>
                <br />
                <a href="https://www.youtube.com/@LearnFromMasters" target="_blank" rel="noopener noreferrer" style={{ color: '#1de9ff', fontWeight: 600, textDecoration: 'underline', display: 'inline-block', marginTop: 8 }}>
          Learn From Masters (YouTube)
                </a>
            </p>
            <h2 style={{ color: '#1de9ff', margin: '56px 0 24px', fontSize: '2em', fontWeight: 700, letterSpacing: 1.2 }}>
        Grands maîtres de la peinture
            </h2>
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
                gap: 48,
                margin: '0 auto 0',
                maxWidth: 1920,
                width: '100%',
                justifyItems: 'center',
                alignItems: 'center',
                padding: '0 2vw'
            }}>
                <img src={'/data/veritable-peintres/dali.jpg'} alt="Dali" style={{ width: '100%', maxWidth: 640, borderRadius: 18, boxShadow: '0 4px 32px #0008', background: '#fff', margin: '0 auto' }} />
                <img src={'/data/veritable-peintres/rembrandt.jpg'} alt="Rembrandt" style={{ width: '100%', maxWidth: 640, borderRadius: 18, boxShadow: '0 4px 32px #0008', background: '#fff', margin: '0 auto' }} />
                <img src={'/data/veritable-peintres/turner.jpg'} alt="Turner" style={{ width: '100%', maxWidth: 640, borderRadius: 18, boxShadow: '0 4px 32px #0008', background: '#fff', margin: '0 auto' }} />
            </div>
            <h2 style={{ color: '#00bcd4', margin: '96px 0 32px', fontSize: '2.2em', fontWeight: 700, letterSpacing: 1.2, textAlign: 'center' }}>
         Mes Peintures
            </h2>
            <div style={{
                background: '#0a2239',
                border: '3px solid #00bcd4',
                borderRadius: 32,
                padding: '48px 2vw 56px',
                margin: '0 auto 64px',
                maxWidth: 2200,
                boxShadow: '0 8px 48px #00bcd422',
                display: 'flex',
                flexWrap: 'wrap',
                justifyContent: 'center',
                alignItems: 'center',
                gap: 56
            }}>
                <img src={'/data/gaby/gaia.JPG'} alt="Peinture Gaby Gaia" style={{ width: '100%', maxWidth: 1200, borderRadius: 24, boxShadow: '0 6px 40px #00bcd488', background: '#fff', margin: '0 12px', border: '2px solid #00bcd4' }} />
                <img src={'/data/gaby/img4.JPG'} alt="Peinture Gaby 4" style={{ width: '100%', maxWidth: 1200, borderRadius: 24, boxShadow: '0 6px 40px #00bcd488', background: '#fff', margin: '0 12px', border: '2px solid #00bcd4' }} />
                <img src={'/data/gaby/marie.JPG'} alt="Peinture Gaby Marie" style={{ width: '100%', maxWidth: 700, borderRadius: 24, boxShadow: '0 6px 40px #00bcd488', background: '#fff', margin: '0 12px', border: '2px solid #00bcd4' }} />
            </div>
        </div>
    );
}
