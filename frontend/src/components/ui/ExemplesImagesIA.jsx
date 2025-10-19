import { useEffect, useState } from 'react';

export default function ExemplesImagesIA() {
    const [galerie, setGalerie] = useState({});

    useEffect(() => {
        fetch('/api/galerie-categories')
            .then((res) => res.json())
            .then((data) => {
                // On retire la catégorie "gaby"
                const filtered = {};
                Object.entries(data).forEach(([cat, images]) => {
                    if (cat.toLowerCase() !== 'gaby') filtered[cat] = images;
                });
                setGalerie(filtered);
            });
    }, []);

    return (
        <div
            style={{
	  width: '100%',
	  maxWidth: 1200,
	  margin: '32px auto 0 auto',
	  background: '#0a2233cc',
	  borderRadius: 18,
	  padding: '32px 4vw',
	  boxShadow: '0 2px 24px #000a',
	  color: '#fff',
	  display: 'flex',
	  flexDirection: 'column',
	  alignItems: 'center',
	  justifyContent: 'center',
	  // maxHeight et overflowY supprimés pour laisser la galerie s'étendre
            }}
        >
            <style>{`
	  @media (max-width: 900px) {
		.galerie-grid {
		  grid-template-columns: repeat(2, 1fr) !important;
		}
	  }
	  @media (max-width: 600px) {
		.galerie-grid {
		  grid-template-columns: 1fr !important;
		}
	  }
	  @media (max-width: 600px) {
		.galerie-img {
		  max-width: 96vw !important;
		}
	  }
	`}</style>
            <h4
                style={{
                    color: '#00bcd4',
                    marginBottom: 18,
                    fontWeight: 700,
                }}
            >
				Exemples d'images générées par l'IA
            </h4>
            {Object.entries(galerie).map(([style, images]) => (
                <div key={style} style={{ width: '100%', marginBottom: 18 }}>
                    <div
                        style={{
                            color: '#7fdfff',
                            fontWeight: 600,
                            marginBottom: 8,
                            fontSize: '1.08em',
                            textAlign: 'center',
                        }}
                    >
                        {style.replaceAll('_', ' ')}
                    </div>
                    <div
	  className="galerie-grid"
	  style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(3, 1fr)',
                            gap: 32,
                            justifyItems: 'center',
                            justifyContent: 'center',
                            width: '100%',
                            margin: '0 auto',
	  }}
                    >
                        {images.map((src) => (
			  <img
                                key={src}
                                src={src
				  .replace('/api/fichier', '/api/images')
				  .replace('?user=images/', '/')
				  .replace('&filename=', '/')}
                                alt={style}
                                className="galerie-img"
                                style={{
				  width: '100%',
				  maxWidth: 320,
				  height: 'auto',
				  aspectRatio: '1/1',
				  borderRadius: 18,
				  boxShadow: '0 4px 24px #000a',
				  background: '#fff',
				  objectFit: 'cover',
				  marginBottom: 10,
				  transition: 'box-shadow 0.2s, transform 0.2s',
                                }}
			  />
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}
