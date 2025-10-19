/*
 * COPYRIGHT (c) 2025 Gaby. Tous droits réservés.
 * Ce code est protégé par le droit d'auteur et ne peut être utilisé, reproduit ou distribué sans autorisation explicite.
 */
  // Cercle bleu nuit juste au-dessus de la numérotation des degrés (placé après les chiffres pour ne pas masquer la roue)
  // (Ce cercle est dessiné après la numérotation pour éviter de masquer la roue ou les chiffres)
// ...existing code...
// (Le second cercle turquoise lumineux sera dessiné à la toute fin de drawWheel)
// Suppression des imports/export pour compatibilité navigateur global
// drawPlanetes doit déjà être sur window
// Ajout du paramètre planetRotationAngles (clé = nom planète, valeur = angle en radians)
window.drawWheel = function(themeData, ctx, canvas, planetImages, signImages, showOuterTurquoiseCircle = true, planetRotationAngles = null) {
  // Initialisation du canvas et des variables
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // Utilise les valeurs passées si présentes, sinon valeurs par défaut
  const cx = (themeData && typeof themeData.cx === 'number') ? themeData.cx : canvas.width / 2;
  const cy = (themeData && typeof themeData.cy === 'number') ? themeData.cy : canvas.height / 2;
  let radius = (themeData && typeof themeData.radius === 'number') ? themeData.radius : (canvas.width / 2 - 120);
  // ...tout le code de dessin de la roue...
  // (Dessin de tous les éléments de la roue ici)
  // Second cercle turquoise lumineux encore plus à l’extérieur (placé à la toute fin, après tout le reste)
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 88, 0, 2 * Math.PI);
  ctx.strokeStyle = '#0099a8'; // turquoise plus sombre
  ctx.lineWidth = 18;
  ctx.globalAlpha = 0.98;
  ctx.shadowColor = 'rgba(0,246,255,0.95)'; // halo turquoise plus intense
  ctx.shadowBlur = 60; // flou beaucoup plus grand
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();
  // Rayon encore réduit pour éloigner la roue des orbites/planètes
  // Rayon réduit pour que la roue ne touche plus les orbites/planètes
  if (radius < 40) radius = 40;
  // Suppression du gradient radial pour éviter tout effet de halo
  console.log('drawWheel appelée', {themeData, planetImages, signImages});
  // ...code de dessin de la roue astrologique...
  // Sécurise tous les arcs pour éviter un rayon négatif
  function safeArc(ctx, cx, cy, r, ...args) {
    if (typeof r === 'number' && r > 0 && isFinite(r)) ctx.arc(cx, cy, r, ...args);
  }
  // ...code de dessin de la roue astrologique...
  // Dessin de la flèche pour l'Ascendant (AS) et du rond pour le Milieu du Ciel (MC) tout à la fin
  // (doit être placé juste avant la fin de la fonction, après tous les autres dessins)
  if (themeData && themeData.points) {
    // Ascendant (AS) : VIOLET avec A blanc
    if (typeof themeData.points.AS === 'number') {
      const angleAS = Math.PI - (themeData.points.AS / 360) * 2 * Math.PI;
      const xAS = cx + (radius + 32) * Math.cos(angleAS);
      const yAS = cy + (radius + 32) * Math.sin(angleAS);
      ctx.save();
      ctx.beginPath();
      ctx.arc(xAS, yAS, 16, 0, 2 * Math.PI);
      ctx.fillStyle = '#a020f0'; // violet
      ctx.globalAlpha = 1.0;
      ctx.shadowColor = '#a020f0';
      ctx.shadowBlur = 14;
      ctx.fill();
      ctx.restore();
      // Texte A blanc au centre
      ctx.save();
      ctx.font = 'bold 20px Arial';
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('A', xAS, yAS);
      ctx.restore();
    }
    // Milieu du Ciel (MC) : TURQUOISE avec M blanc
    if (typeof themeData.points.MC === 'number') {
      const angleMC = Math.PI - (themeData.points.MC / 360) * 2 * Math.PI;
      const xMC = cx + (radius + 32) * Math.cos(angleMC);
      const yMC = cy + (radius + 32) * Math.sin(angleMC);
      ctx.save();
      ctx.beginPath();
      ctx.arc(xMC, yMC, 16, 0, 2 * Math.PI);
      ctx.fillStyle = '#00e5ff'; // turquoise
      ctx.globalAlpha = 1.0;
      ctx.shadowColor = '#00e5ff';
      ctx.shadowBlur = 14;
      ctx.fill();
      ctx.restore();
      // Texte M blanc au centre
      ctx.save();
      ctx.font = 'bold 20px Arial';
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('M', xMC, yMC);
      ctx.restore();
    }
  }
  // Fond bleu uni minimaliste (pas de halo ni de dégradé)
  ctx.save();
  ctx.beginPath();
  ctx.rect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#0a1220';
  ctx.globalAlpha = 1.0;
  ctx.fill();
  ctx.restore();
  // Graduation zodiacale sur le cercle extérieur principal (radius + 80), tourne en sens opposé à la roue
  const zodiacGradRadius = radius + 80;
  // Multiplie la vitesse de rotation des ticks pour un effet plus visible
  const rotationTicks = (themeData && typeof themeData.roueRotation === 'number') ? -2 * themeData.roueRotation : 0;
  for (let i = 0; i < 12; i++) {
    // Ajoute la rotation opposée pour les ticks
    const angle = Math.PI - ((i + 0.5) * 30 / 360) * 2 * Math.PI + (rotationTicks * Math.PI / 180);
    const x1 = cx + (zodiacGradRadius - 18) * Math.cos(angle);
    const y1 = cy + (zodiacGradRadius - 18) * Math.sin(angle);
    const x2 = cx + (zodiacGradRadius + 18) * Math.cos(angle);
    const y2 = cy + (zodiacGradRadius + 18) * Math.sin(angle);
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = '#00e5ff';
    ctx.lineWidth = 3.2;
    ctx.globalAlpha = 1.0;
    ctx.shadowColor = 'rgba(0,0,0,0)'; // Suppression du halo
    ctx.shadowBlur = 0;
    ctx.stroke();
    ctx.restore();
  }
  // Graduation zodiacale à l'intérieur du cercle intérieur des signes (invisible)
  // const zodiacGradRadius = radius - 110;
  // for (let i = 0; i < 12; i++) {
  //   const angle = Math.PI - ((i + 0.5) * 30 / 360) * 2 * Math.PI;
  //   const x1 = cx + (zodiacGradRadius - 8) * Math.cos(angle);
  //   const y1 = cy + (zodiacGradRadius - 8) * Math.sin(angle);
  //   const x2 = cx + (zodiacGradRadius + 8) * Math.cos(angle);
  //   const y2 = cy + (zodiacGradRadius + 8) * Math.sin(angle);
  //   ctx.save();
  //   ctx.beginPath();
  // Initialisation du canvas et des variables
  //   ctx.lineTo(x2, y2);
  //   ctx.strokeStyle = '#00e5ff';
  //   ctx.lineWidth = 3.2;
  //   ctx.globalAlpha = 0.0; // invisible
  // Dessin de la flèche pour l'Ascendant (AS) et du rond pour le Milieu du Ciel (MC)
  //   ctx.restore();
  // }
  // (halo/gradient supprimé, fond bleu uni déjà appliqué plus haut)

  // Cercle principal turquoise bien visible autour de la roue


  // Cercle turquoise principal avec halo lumineux ENCORE PLUS EPAIS ET LUMINEUX
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius, 0, 2 * Math.PI);
  ctx.strokeStyle = '#00f6ff'; // turquoise encore plus clair
  ctx.lineWidth = 72; // encore plus épais
  ctx.globalAlpha = 1.0;
  ctx.shadowColor = 'rgba(0,246,255,1)'; // halo encore plus lumineux
  ctx.shadowBlur = 120; // flou encore plus grand
  ctx.stroke();
  ctx.restore();

  // Plusieurs cercles bleu sombre très fins juste au-dessus du cercle turquoise principal
  for (let offset = 2; offset <= 10; offset += 2) {
    ctx.save();
    ctx.beginPath();
    safeArc(ctx, cx, cy, radius + offset, 0, 2 * Math.PI);
    ctx.strokeStyle = '#0a2a4d'; // bleu sombre
    ctx.lineWidth = 7; // encore plus épais
    ctx.globalAlpha = 0.92;
    ctx.shadowColor = 'rgba(0,246,255,0.25)'; // halo bleu clair subtil
    ctx.shadowBlur = 18;
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.restore();
  }


  // Halo lumineux turquoise autour du cercle principal


  // Cercle bleu nuit très fin avec halo bleu nuit subtil pour la numérotation
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 4, 0, 2 * Math.PI);
  ctx.strokeStyle = '#0a2a4d'; // bleu nuit
  ctx.lineWidth = 2.2; // plus fin
  ctx.globalAlpha = 0.92;
  ctx.shadowColor = 'rgba(10,42,77,0.22)'; // halo bleu nuit subtil
  ctx.shadowBlur = 10;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Plusieurs cercles bleu nuit très fins juste au-dessus du cercle de numérotation
  for (let offset = 6; offset <= 16; offset += 2) {
    ctx.save();
    ctx.beginPath();
    safeArc(ctx, cx, cy, radius + offset, 0, 2 * Math.PI);
    ctx.strokeStyle = '#0a2a4d'; // bleu nuit
    ctx.lineWidth = 1.1;
    ctx.globalAlpha = 0.85;
    ctx.shadowColor = 'rgba(10,42,77,0.13)'; // halo bleu nuit très subtil
    ctx.shadowBlur = 6;
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.restore();
  }

  // Cercle bleu nuit très fin juste au-dessus du cercle turquoise (proche de la numérotation)
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 6, 0, 2 * Math.PI);
  ctx.strokeStyle = '#0a2a4d'; // bleu nuit
  ctx.lineWidth = 1.2;
  ctx.globalAlpha = 0.92;
  ctx.shadowColor = 'rgba(10,42,77,0.13)'; // halo bleu nuit subtil
  ctx.shadowBlur = 6;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Cercle bleu nuit épais juste au-dessus du cercle de numérotation
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 8, 0, 2 * Math.PI);
  ctx.strokeStyle = '#0a2a4d'; // bleu nuit
  ctx.lineWidth = 13;
  ctx.globalAlpha = 0.92;
  ctx.shadowColor = 'rgba(10,42,77,0.18)'; // halo bleu nuit subtil
  ctx.shadowBlur = 8;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Plusieurs cercles dorés très fins juste au-dessus du cercle turquoise, montant plus haut
  for (let offset = 8; offset <= 40; offset += 2) {
    ctx.save();
    ctx.beginPath();
    safeArc(ctx, cx, cy, radius + offset, 0, 2 * Math.PI);
    ctx.strokeStyle = '#FFD700'; // doré
    ctx.lineWidth = 1.1;
    ctx.globalAlpha = 0.92;
    ctx.shadowColor = 'rgba(0,0,0,0)';
    ctx.shadowBlur = 0;
    ctx.stroke();
    ctx.restore();
  }

  // Cercle bleu nuit qui ferme les secteurs des signes
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 18, 0, 2 * Math.PI);
  ctx.strokeStyle = '#0a2a4d'; // bleu nuit
  ctx.lineWidth = 6.5;
  ctx.globalAlpha = 0.98;
  ctx.shadowColor = 'rgba(10,42,77,0.32)'; // halo bleu nuit subtil
  ctx.shadowBlur = 14;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Trois cercles dorés très fins à l'intérieur du cercle intérieur de la roue
  for (let offset = 8; offset <= 24; offset += 8) {
    ctx.save();
    ctx.beginPath();
    safeArc(ctx, cx, cy, radius - offset, 0, 2 * Math.PI);
    ctx.strokeStyle = '#FFD700'; // doré
    ctx.lineWidth = 1.2;
    ctx.globalAlpha = 0.95;
    ctx.shadowColor = 'rgba(0,0,0,0)';
    ctx.shadowBlur = 0;
    ctx.stroke();
    ctx.restore();
  }

  // Trois cercles dorés très fins à l'extérieur du cercle intérieur de la roue (zone des aspects)
  for (let offset = 60; offset <= 76; offset += 8) {
    ctx.save();
    ctx.beginPath();
    safeArc(ctx, cx, cy, radius + offset, 0, 2 * Math.PI);
    ctx.strokeStyle = '#FFD700'; // doré
    ctx.lineWidth = 1.2;
    ctx.globalAlpha = 0.95;
    ctx.shadowColor = 'rgba(0,0,0,0)';
    ctx.shadowBlur = 0;
    ctx.stroke();
    ctx.restore();
  }
  // Dernier cercle turquoise lumineux juste au-dessus des trois cercles dorés extérieurs
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 80, 0, 2 * Math.PI);
  ctx.strokeStyle = '#0a2a4d'; // bleu nuit subtil
  ctx.lineWidth = 18;
  ctx.globalAlpha = 0.75;
  ctx.shadowColor = 'rgba(10,42,77,0.18)'; // halo bleu nuit léger
  ctx.shadowBlur = 18;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Trois cercles dorés très fins autour du premier cercle intérieur (radius - 100)
  // Cercles dorés rapprochés autour du premier cercle intérieur (radius - 100, -102, -104)
  for (let offset = 0; offset <= 10; offset += 2) {
    ctx.save();
    ctx.beginPath();
    safeArc(ctx, cx, cy, radius - 100 - offset, 0, 2 * Math.PI);
    ctx.strokeStyle = '#FFD700'; // doré
    ctx.lineWidth = 1.2;
    ctx.globalAlpha = 0.95;
    ctx.shadowColor = 'rgba(0,0,0,0)';
    ctx.shadowBlur = 0;
    ctx.stroke();
    ctx.restore();
  }

  // Ajout de 3 cercles supplémentaires
  // Cercle 1 (proche du cercle turquoise)
  // Cercle 1 (proche du cercle turquoise) rendu invisible
  // ctx.save();
  // ctx.beginPath();
  // ctx.arc(cx, cy, radius + 15, 0, 2 * Math.PI);
  // ctx.strokeStyle = 'rgba(0,0,0,0)';
  // ctx.lineWidth = 0;
  // ctx.globalAlpha = 0;
  // ctx.shadowColor = 'rgba(0,0,0,0)';
  // ctx.shadowBlur = 0;
  // ctx.stroke();
  // ctx.restore();
  // Cercle bleu nuit juste sous la numérotation des degrés
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 42, 0, 2 * Math.PI);
  ctx.strokeStyle = '#0a2a4d'; // bleu nuit
  ctx.lineWidth = 22;
  ctx.globalAlpha = 0.92;
  ctx.shadowColor = 'rgba(10,42,77,0.18)'; // halo bleu nuit subtil
  ctx.shadowBlur = 10;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Numérotation des degrés (0°, 10°, ..., 350°) sans ticks autour du cercle bleu nuit
  const zodiacDegTextRadius = radius + 44;
  for (let i = 0; i < 36; i++) {
    const angle = Math.PI - ((i + 0.5) * 10 / 360) * 2 * Math.PI;
    const xText = cx + zodiacDegTextRadius * Math.cos(angle);
    const yText = cy + zodiacDegTextRadius * Math.sin(angle);
    ctx.save();
    ctx.font = 'bold 13px Arial';
    ctx.fillStyle = '#fff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.globalAlpha = 0.92;
    ctx.fillText(`${i * 10}°`, xText, yText);
    ctx.restore();
  }

  // Cercle 2 (milieu)
  // Cercle 2 (milieu) rendu invisible
  // ctx.save();
  // ctx.beginPath();
  // ctx.arc(cx, cy, radius + 28, 0, 2 * Math.PI);
  // ctx.strokeStyle = 'rgba(0,0,0,0)';
  // ctx.lineWidth = 0;
  // ctx.globalAlpha = 0;
  // ctx.shadowColor = 'rgba(0,0,0,0)';

  // Nouveau cercle extérieur pour entourer les planètes
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 50, 0, 2 * Math.PI);
  ctx.strokeStyle = '#ffe066';
  ctx.lineWidth = 3.5;
  ctx.globalAlpha = 0.7;
  ctx.shadowColor = 'rgba(0,0,0,0)'; // Suppression du halo
  ctx.shadowBlur = 0;
  ctx.stroke();
  ctx.restore();
  // Cercle turquoise lumineux juste au-dessus du cercle extérieur
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 54, 0, 2 * Math.PI);
  ctx.strokeStyle = '#00f6ff'; // turquoise clair
  ctx.lineWidth = 7.5;
  ctx.globalAlpha = 0.95;
  ctx.shadowColor = 'rgba(0,246,255,0.85)';
  ctx.shadowBlur = 32;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Cercle 3 (proche du cercle blanc extérieur)
  // Cercle 3 (proche du cercle blanc extérieur) rendu invisible
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 36, 0, 2 * Math.PI);
  ctx.strokeStyle = '#FFD700'; // doré
  ctx.lineWidth = 1.2; // très fin
  ctx.globalAlpha = 0.95;
  ctx.shadowColor = 'rgba(0,0,0,0)'; // pas d'effet astral
  ctx.shadowBlur = 0;
  ctx.stroke();
  ctx.restore();


  // ...cercles d'orbite turquoise retirés à la demande de l'utilisateur...

  // Ajout d'un cercle extérieur supplémentaire
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius + 40, 0, 2 * Math.PI);
  ctx.strokeStyle = '#0a2a4d'; // bleu nuit
  ctx.lineWidth = 3.5;
  ctx.globalAlpha = 0.7;
  ctx.shadowColor = 'rgba(0,0,0,0)'; // Suppression du halo
  ctx.shadowBlur = 0;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Graduations des 12 maisons selon les cuspides dynamiques
  const cusps = (themeData && Array.isArray(themeData.maisons_deg) && themeData.maisons_deg.length === 12)
    ? themeData.maisons_deg
    : (themeData && Array.isArray(themeData.cusps) && themeData.cusps.length === 12)
      ? themeData.cusps
      : null;
  // Suppression du trait blanc sur chaque cuspide de maison (géré par drawMaisons.js)

  // Cercle bleu nuit à l'intérieur de la roue (plus proche du centre)
  ctx.save();
  ctx.beginPath();
  safeArc(ctx, cx, cy, radius - 100, 0, 2 * Math.PI);
  ctx.strokeStyle = '#0a2a4d'; // bleu nuit
  ctx.lineWidth = 3.5;
  ctx.globalAlpha = 0.92;
  ctx.shadowColor = 'rgba(10,42,77,0.13)'; // halo bleu nuit subtil
  ctx.shadowBlur = 8;
  ctx.stroke();
  ctx.shadowBlur = 0;
  ctx.restore();

  // Remplissage des secteurs des signes avec un dégradé turquoise
  let innerSignRadius = radius - 100;
  let outerSignRadius = radius;
  // Sécurise les rayons pour le gradient
  if (innerSignRadius < 1) innerSignRadius = 1;
  if (outerSignRadius < innerSignRadius + 1) outerSignRadius = innerSignRadius + 1;
  for (let i = 0; i < 12; i++) {
    const startAngle = Math.PI - (i * 30 / 360) * 2 * Math.PI;
    const endAngle = Math.PI - ((i + 1) * 30 / 360) * 2 * Math.PI;
    // Rétablissement du remplissage turquoise dégradé
    const grad = ctx.createRadialGradient(cx, cy, innerSignRadius, cx, cy, outerSignRadius);
    grad.addColorStop(0, '#00e5ff'); // turquoise vif
    grad.addColorStop(1, '#2979ff'); // bleu astral
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, outerSignRadius, startAngle, endAngle, true);
    ctx.arc(cx, cy, innerSignRadius, endAngle, startAngle, false);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.globalAlpha = 0.38;
    ctx.fill();
    ctx.restore();
    // Délimitation du secteur
    const x1 = cx + innerSignRadius * Math.cos(startAngle);
    const y1 = cy + innerSignRadius * Math.sin(startAngle);
    const x2 = cx + (outerSignRadius + 18) * Math.cos(startAngle);
    const y2 = cy + (outerSignRadius + 18) * Math.sin(startAngle);
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.strokeStyle = '#0a2a4d'; // bleu nuit
    ctx.lineWidth = 2.5; // plus fin qu'avant
    ctx.globalAlpha = 0.92;
    ctx.shadowColor = 'rgba(10,42,77,0.13)'; // halo bleu nuit très subtil
    ctx.shadowBlur = 6;
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.restore();
    // Petites graduations intermédiaires tous les 5°
    for (let j = 1; j < 6; j++) {
      const deg = i * 30 + j * 5;
      // Suppression des halos et cercles turquoise extérieurs
      const angleGrad = Math.PI - (deg / 360) * 2 * Math.PI;
      const xGrad1 = cx + (outerSignRadius - 6) * Math.cos(angleGrad);
      const yGrad1 = cy + (outerSignRadius - 6) * Math.sin(angleGrad);
      const xGrad2 = cx + (outerSignRadius + 8) * Math.cos(angleGrad);
      const yGrad2 = cy + (outerSignRadius + 8) * Math.sin(angleGrad);
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(xGrad1, yGrad1);
      ctx.lineTo(xGrad2, yGrad2);
      ctx.strokeStyle = '#00e5ff';
      ctx.lineWidth = 1.2;
      ctx.globalAlpha = 0.45;
      ctx.shadowColor = 'rgba(0,0,0,0)'; // Suppression du halo
      ctx.shadowBlur = 0;
      ctx.stroke();
      ctx.restore();
    }
  }

  // Dessin des signes avec couleurs du themeData (comme VS Code/SVG)
  console.log('[DEBUG] themeData:', themeData);
  console.log('[DEBUG] signs_glyphs_colors:', themeData ? themeData.signs_glyphs_colors : 'themeData undefined');
  
  if (themeData && themeData.signs_glyphs_colors) {
    console.log('[DEBUG] Couleurs des signes trouvées!', themeData.signs_glyphs_colors);
    const signNames = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                       'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
    const signGlyphs = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓'];
    
    for (let i = 0; i < 12; i++) {
      const sectorAngle = 30;
      const angle = Math.PI - ((i + 0.5) * sectorAngle / 360) * 2 * Math.PI;
      const x = cx + (radius - 60) * Math.cos(angle);
      const y = cy + (radius - 60) * Math.sin(angle);
      const signName = signNames[i];
      const signGlyph = signGlyphs[i];
      const signColor = themeData.signs_glyphs_colors[signName] || '#ffffff';
      
      ctx.save();
      ctx.font = 'bold 32px Arial';
      ctx.fillStyle = signColor;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.globalAlpha = 1.0;
      ctx.shadowColor = signColor;
      ctx.shadowBlur = 8;
      ctx.fillText(signGlyph, x, y);
      ctx.restore();
    }
  }
  // Fallback: Dessin des signes avec images si pas de couleurs dans themeData
  else if (signImages && Array.isArray(signImages) && signImages.length === 12) {
    console.log('[DEBUG] Pas de couleurs trouvées, utilisation des images des signes');
    for (let i = 0; i < 12; i++) {
      const sectorAngle = 30;
      const angle = Math.PI - ((i + 0.5) * sectorAngle / 360) * 2 * Math.PI;
      const x = cx + (radius - 60) * Math.cos(angle);
      const y = cy + (radius - 60) * Math.sin(angle);
      const img = signImages[i];
      if (img) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(angle + Math.PI / 2);
        ctx.beginPath();
        ctx.arc(0, 0, 32, 0, 2 * Math.PI); // rayon réduit
        ctx.clip();
        ctx.drawImage(img, -28, -28, 56, 56); // taille réduite
        ctx.restore();
      }
    }
  }
  else {
    console.log('[DEBUG] Ni couleurs ni images des signes disponibles');
    console.log('[DEBUG] themeData:', !!themeData);
    console.log('[DEBUG] signImages:', signImages);
  }


  // Dessin des aspects à l'intérieur du dernier cercle (radius - 30), positions animées pour test
  if (themeData && themeData.aspects && Array.isArray(themeData.aspects) && themeData.planetes) {
    const aspectRadius = radius - 30;
    for (const aspect of themeData.aspects) {
      const { from, to, type } = aspect;
      // Utilise les positions animées pour garantir la visibilité
      const degFrom = themeData.planetes[from];
      const degTo = themeData.planetes[to];
      if (typeof degFrom === 'number' && typeof degTo === 'number') {
        const angleFrom = Math.PI - (degFrom / 360) * 2 * Math.PI;
        const angleTo = Math.PI - (degTo / 360) * 2 * Math.PI;
        const x1 = cx + aspectRadius * Math.cos(angleFrom);
        const y1 = cy + aspectRadius * Math.sin(angleFrom);
        const x2 = cx + aspectRadius * Math.cos(angleTo);
        const y2 = cy + aspectRadius * Math.sin(angleTo);
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = type === 'conjunction' ? '#ffd600' : (type === 'opposition' ? '#ff1744' : '#00e676');
        ctx.lineWidth = 4.2;
        ctx.globalAlpha = 1.0;
        ctx.shadowColor = 'rgba(0,0,0,0)'; // Suppression du halo
        ctx.shadowBlur = 0;
        ctx.setLineDash(type === 'conjunction' ? [] : [8, 6]);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.shadowBlur = 0;
        ctx.restore();
      }
    }
  }

  // ...fin du code de dessin de la roue...
  // Les planètes ne sont plus dessinées sur le cercle turquoise principal
  // Dessin des planètes avec images
  console.log('planetImages:', planetImages);
  console.log('themeData.planetes:', themeData && themeData.planetes);
  if (planetImages && Array.isArray(planetImages) && planetImages.length > 0 && themeData && themeData.planetes) {
    const planetNames = [
      'sun','moon','mercury','venus','mars','jupiter','saturn','uranus','neptune','pluto','chiron','north-node','part-of-fortune'
    ];
    const planetKeys = [
      'Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','North Node','Part of Fortune'
    ];
    const baseRadius = radius; // Place les planètes sur le cercle turquoise principal
    for (let i = 0; i < planetNames.length; i++) {
      const planetKey = planetKeys[i];
      const deg = themeData.planetes[planetKey];
      // Utilise le dossier public/planetes_mini pour les images
      const imgPath = `/planetes_mini/${planetNames[i]}.png`;
      const img = new window.Image();
      img.src = imgPath;
      if (typeof deg === 'number') {
        // Ajoute la rotation individuelle si fournie
        let extraAngle = 0;
        if (planetRotationAngles && typeof planetRotationAngles[planetKey] === 'number') {
          extraAngle = planetRotationAngles[planetKey]; // en radians
        }
        const angleRad = Math.PI - (deg / 360) * 2 * Math.PI + extraAngle;
        const x = cx + baseRadius * Math.cos(angleRad);
        const y = cy + baseRadius * Math.sin(angleRad);
        // Log pour debug
        console.log('PLANETE', planetKey, 'deg:', deg, 'x:', x, 'y:', y);
        // Tick jaune en V sur le cercle halo (radius + 80)
        ctx.save();
        ctx.translate(cx + tickRadius * Math.cos(angleRad), cy + tickRadius * Math.sin(angleRad));
        ctx.rotate(angleRad + Math.PI / 2);
        ctx.beginPath();
        ctx.moveTo(0, -12); // pointe du V
        ctx.lineTo(6, 6);   // branche droite
        ctx.lineTo(-6, 6);  // branche gauche
        ctx.closePath();
        ctx.strokeStyle = '#fff200'; // jaune astral plus vif
        ctx.lineWidth = 3.2;
        ctx.globalAlpha = 1.0;
        ctx.shadowColor = 'rgba(0,0,0,0)'; // Suppression du halo
        ctx.shadowBlur = 0;
        ctx.stroke();
        ctx.restore();
        // Affiche un cercle de secours à chaque passage
        ctx.save();
        ctx.beginPath();
        ctx.arc(x, y, 18, 0, 2 * Math.PI);
        ctx.strokeStyle = '#ff1744';
        ctx.lineWidth = 2.5;
        ctx.globalAlpha = 0.8;
        ctx.shadowColor = 'rgba(0,0,0,0)'; // Suppression du halo
        ctx.shadowBlur = 0;
        ctx.stroke();
        ctx.font = 'bold 13px Arial';
        ctx.fillStyle = '#ff1744';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(planetKey[0], x, y);
        ctx.restore();
        img.onload = function() {
          ctx.save();
          ctx.translate(x, y);
          ctx.rotate(angleRad + Math.PI / 2);
          ctx.beginPath();
          ctx.arc(0, 0, 18, 0, 2 * Math.PI); // plus petit
          ctx.clip();
          ctx.drawImage(img, -16, -16, 32, 32); // plus petit
          ctx.restore();
        };
      }
    }
  }
  // ...fin du code de dessin de la roue...
}

// Dessine la roue astrologique en appliquant une rotation globale (pour l'animation)
window.drawWheelRotating = function(themeData, ctx, canvas, planetImages, signImages, angle) {
  ctx.save();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.translate(canvas.width / 2, canvas.height / 2);
  ctx.rotate(angle);
  ctx.translate(-canvas.width / 2, -canvas.height / 2);
  // Passe le themeData pour avoir les couleurs des signes comme le SVG
  window.drawWheel(themeData || {}, ctx, canvas, planetImages, signImages);
  ctx.restore();
}

window.drawSignes = function(images, ctx, canvas) {
  // ...code existant...
}
