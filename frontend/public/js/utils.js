// Module : Fonctions utilitaires pour la roue astrologique
// Utilisation : import { getCirclePosition, degToRad } from './utils.js'

export function getCirclePosition(cx, cy, radius, deg) {
  // Retourne {x, y} sur le cercle pour un angle en degrés
  const rad = degToRad(deg);
  return {
    x: cx + radius * Math.cos(rad),
    y: cy + radius * Math.sin(rad)
  };
}

export function degToRad(deg) {
  return Math.PI - (deg / 360) * 2 * Math.PI;
}
