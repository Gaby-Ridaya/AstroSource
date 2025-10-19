import { useEffect, useState } from 'react';

export default function GalerieCategories() {
    const [galerie, setGalerie] = useState({});
    const [zoomUrl, setZoomUrl] = useState(null);

    useEffect(() => {
        fetch('/api/galerie-categories')
            .then(res => res.json())
            .then(data => setGalerie(data.galerie || {}));
    }, []);

    return (
        <div style={{ padding: 32 }}>
            {Object.entries(galerie)
                .filter(([categorie]) => categorie !== 'gaby')
                .map(([categorie, images]) => {
                    const imagesList = Array.isArray(images) ? images : [];
                    return (
                        <div key={categorie} style={{ marginBottom: 48 }}>
                            <h2 style={{ color: '#00bcd4', fontWeight: 700, marginBottom: 16, fontSize: '2em' }}>
                                {`Créations IA : ${categorie.replaceAll('_', ' ')}`}
                            </h2>
                            <div
                                style={{
                                    display: 'grid',
                                    gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
                                    gap: 32,
                                    alignItems: 'center'
                                }}
                            >
                                {imagesList.map(url => (
                                    <img
                                        key={url}
                                        src={`http://localhost:8000/images/${categorie}/${url}`}
                                        alt={categorie}
                                        style={{
                                            width: '100%',
                                            maxWidth: 340,
                                            aspectRatio: '1/1',
                                            borderRadius: 16,
                                            boxShadow: '0 2px 24px #0004',
                                            background: '#fff',
                                            objectFit: 'cover',
                                            transition: 'transform 0.2s, box-shadow 0.2s',
                                            cursor: 'zoom-in'
                                        }}
                                        onClick={() => setZoomUrl(`http://localhost:8000/images/${categorie}/${url}`)}
                                        onMouseOver={e => {
                                            e.currentTarget.style.transform = 'scale(1.04)';
                                            e.currentTarget.style.boxShadow = '0 4px 32px #00bcd455';
                                        }}
                                        onMouseOut={e => {
                                            e.currentTarget.style.transform = 'scale(1)';
                                            e.currentTarget.style.boxShadow = '0 2px 24px #0004';
                                        }}
                                    />
                                ))}
                            </div>
                            {zoomUrl && (
                                <div
                                    onClick={() => setZoomUrl(null)}
                                    style={{
                                        position: 'fixed',
                                        top: 0,
                                        left: 0,
                                        width: '100vw',
                                        height: '100vh',
                                        background: 'rgba(10,34,51,0.92)',
                                        zIndex: 2000,
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        cursor: 'zoom-out'
                                    }}
                                >
                                    <img
                                        src={zoomUrl}
                                        alt="Agrandissement"
                                        style={{
                                            maxWidth: '90vw',
                                            maxHeight: '90vh',
                                            borderRadius: 20,
                                            boxShadow: '0 4px 48px #00bcd4cc, 0 2px 32px #000a',
                                            background: '#fff'
                                        }}
                                    />
                                </div>
                            )}
                        </div>
                    );
                })}
        </div>
    );
}
