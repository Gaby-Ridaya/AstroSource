// Animation de la roue astrologique :
// - Sur la page d'accueil : tourne en continu
// - Sur la page astro_roue.html : tourne puis s'arrête sur le thème utilisateur

import { drawWheel, drawWheelRotating } from '/static/js/drawWheel.js';

// Animation pour la page d'accueil (roue générique qui tourne en continu)
export function startAccueilWheelAnimation(ctx, canvas, planetImages, signImages) {
  let angle = 0;
  function animate() {
    drawWheelRotating(ctx, canvas, planetImages, signImages, angle);
    angle += 0.02;
    requestAnimationFrame(animate);
  }
  animate();
}

// Animation pour la page astro_roue.html (tourne puis s'arrête sur le thème)
export function startAstroRoueAnimation(ctx, canvas, planetImages, signImages, onThemeLoaded) {
  let angle = 0;
  let animationId = null;
  let themeLoaded = false;

  function animate() {
    if (themeLoaded) return;
    drawWheelRotating(ctx, canvas, planetImages, signImages, angle);
    angle += 0.02;
    animationId = requestAnimationFrame(animate);
  }

  // Lance l'animation
  animate();

  // Fonction à appeler quand le thème est chargé
  function stopAndDrawTheme(themeData) {
    themeLoaded = true;
    if (animationId) cancelAnimationFrame(animationId);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawWheel(themeData, ctx, canvas, planetImages, signImages);
  }

  // onThemeLoaded doit appeler stopAndDrawTheme(themeData)
  return stopAndDrawTheme;
}

// Exemple d'utilisation dans astro_roue.html :
// const stopAndDrawTheme = startAstroRoueAnimation(ctx, canvas, planetImages, signImages);
// ...
// Quand le thème est chargé : stopAndDrawTheme(themeData);
