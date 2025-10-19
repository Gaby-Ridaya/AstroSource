export default function YoutubeVideos() {
    return (
        <div style={{ padding: 40, color: '#fff', fontFamily: 'Orbitron, Arial, sans-serif', textAlign: 'center' }}>
            <h2 style={{ color: '#12c5d5fb', fontSize: '2.2em', marginBottom: 24, textShadow: '0 2px 16px #088cd8ff, 0 1px 2px #000a' }}>
        Mes vidéos
            </h2>
            <p style={{ fontSize: '1.1em', marginBottom: 32 }}>
        Retrouvez ici une sélection de mes vidéos &nbsp;!
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 32 }}>
                {/* Vidéos YouTube réelles */}
                <iframe width="800" height="450" src="https://www.youtube.com/embed/6LMcYSVcMHA" title="Astrologie Vidéo 1" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
                <iframe width="800" height="450" src="https://www.youtube.com/embed/DRYk9HaVgFg" title="Astrologie Vidéo 2" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
                <iframe width="800" height="450" src="https://www.youtube.com/embed/o7R8Onj5b7s" title="Astrologie Vidéo 3" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
                <iframe width="800" height="450" src="https://www.youtube.com/embed/XV-d1smX6tI" title="Astrologie Vidéo 4" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
            </div>
        </div>
    );
}
