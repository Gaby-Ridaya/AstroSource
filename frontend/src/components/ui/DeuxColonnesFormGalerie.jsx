import React from 'react';
import './deuxColonnes.css';

export default function DeuxColonnesFormGalerie({ children, form, galerie }) {
    return (
        <div className="deux-colonnes-container">
            <div className="colonne-formulaire">
                {form}
            </div>
            {galerie && (
                <div className="colonne-galerie">
                    {galerie}
                </div>
            )}
        </div>
    );
}
