import React, { useEffect } from 'react';

const NB_ETOILES = 120; // Mets-en plus si tu veux un univers Marvel

export default function SuperEtoiles() {
    useEffect(() => {
        const container = document.getElementById('etoiles');
        if (!container) return;
        container.innerHTML = ''; // Clear les étoiles précédentes si reload

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
