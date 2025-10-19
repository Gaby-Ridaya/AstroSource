// Exemple d'intégration pour redessiner la roue astrologique
// Place ce code dans ton JS principal (pas dans drawWheel.js)

import { drawWheel } from './drawWheel.js';

// Récupère le canvas et le contexte
const canvas = document.getElementById('tonCanvasId'); // Remplace par l'ID réel
const ctx = canvas.getContext('2d');

// Variables globales (à adapter selon ton projet)
let themeData = {}; // Tes données astrologiques
let planetImages = []; // Tes images de planètes
let signImages = []; // Tes images de signes

// Fonction pour redessiner la roue
function redrawWheel() {
  console.log('drawWheel appelé', { themeData, planetImages, signImages });
  drawWheel(themeData, ctx, canvas, planetImages, signImages);
}

// Redessine à chaque resize de la fenêtre
window.addEventListener('resize', () => {
  // Optionnel : adapte la taille du canvas
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  redrawWheel();
});

// Redessine à chaque changement de données astrologiques
function onThemeDataChange(newThemeData) {
  themeData = newThemeData;
  redrawWheel();
}

// Redessine à chaque chargement d'images
function onImagesLoaded(newPlanetImages, newSignImages) {
  planetImages = newPlanetImages;
  signImages = newSignImages;
  redrawWheel();
}

// Appelle redrawWheel() au démarrage
redrawWheel();
