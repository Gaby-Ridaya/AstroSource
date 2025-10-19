// Module : Dessin des planètes et des ticks
// Utilisation : drawPlanetes(ctx, params)

window.drawPlanetes = function(ctx, params) {
  // ctx : contexte canvas
  // params : {cx, cy, radius, planetes, images} ou {themeData: {planetes}, ...}
  // Dessine les planètes et les ticks sur la roue
  if (!params || (!params.planetes && !(params.themeData && params.themeData.planetes)) || !params.images) return;
  const planetes = params.planetes || (params.themeData && params.themeData.planetes);
  const cx = params.cx;
  const cy = params.cy;
  const radius = params.radius; // correction : ajout de la variable
  // Place les planètes sur le cercle turquoise principal
  const baseRadius = radius; // cercle turquoise
  const planetNames = Object.keys(planetes);
  for (let i = 0; i < planetNames.length; i++) {
    const planet = planetNames[i];
    const deg = planetes[planet];
    const img = params.images[planet]; // mapping par nom
    if (typeof deg === 'number') {
      const angleRad = Math.PI - (deg / 360) * 2 * Math.PI;
      const x = cx + baseRadius * Math.cos(angleRad);
      const y = cy + baseRadius * Math.sin(angleRad);
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(angleRad + Math.PI / 2);
      if (img) {
        ctx.beginPath();
        ctx.arc(0, 0, 14, 0, 2 * Math.PI); // plus petit
        ctx.clip();
        ctx.drawImage(img, -14, -14, 28, 28); // plus petit
        // Affiche le degré sous l'image
        ctx.font = '12px sans-serif';
        ctx.fillStyle = '#fff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText(deg + '°', 0, 16);
      }
      ctx.restore();
    }
  }
}

// Module pour dessiner les planètes et les repères AS/MC
window.drawPlanetesFromJson = function(json, ctx, canvas) {
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const radius = canvas.width / 2 - 180;
  const rV = radius - 20;
  const vSize = 32;
  // AS
  if (json && typeof json.ascendant === 'number') {
    const asDeg = json.ascendant;
    const asAngleRad = Math.PI - (asDeg / 360) * 2 * Math.PI;
    const xV_as = cx + rV * Math.cos(asAngleRad);
    const yV_as = cy + rV * Math.sin(asAngleRad);
    const angleLeft_as = asAngleRad - Math.PI / 36;
    const angleRight_as = asAngleRad + Math.PI / 36;
    const xLeft_as = xV_as + vSize * Math.cos(angleLeft_as);
    const yLeft_as = yV_as + vSize * Math.sin(angleLeft_as);
    const xRight_as = xV_as + vSize * Math.cos(angleRight_as);
    const yRight_as = yV_as + vSize * Math.sin(angleRight_as);
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(xLeft_as, yLeft_as);
    ctx.lineTo(xV_as, yV_as);
    ctx.lineTo(xRight_as, yRight_as);
    ctx.strokeStyle = '#2979ff';
    ctx.lineWidth = 3.2;
    ctx.shadowColor = '#fff';
    ctx.shadowBlur = 8;
    ctx.globalAlpha = 0.98;
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.globalAlpha = 1;
    ctx.restore();
  }
  // MC
  if (json && typeof json.mc === 'number') {
    const mcDeg = json.mc;
    const mcAngleRad = Math.PI - (mcDeg / 360) * 2 * Math.PI;
    const xV_mc = cx + rV * Math.cos(mcAngleRad);
    const yV_mc = cy + rV * Math.sin(mcAngleRad);
    const angleLeft_mc = mcAngleRad - Math.PI / 36;
    const angleRight_mc = mcAngleRad + Math.PI / 36;
    const xLeft_mc = xV_mc + vSize * Math.cos(angleLeft_mc);
    const yLeft_mc = yV_mc + vSize * Math.sin(angleLeft_mc);
    const xRight_mc = xV_mc + vSize * Math.cos(angleRight_mc);
    const yRight_mc = yV_mc + vSize * Math.sin(angleRight_mc);
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(xLeft_mc, yLeft_mc);
    ctx.lineTo(xV_mc, yV_mc);
    ctx.lineTo(xRight_mc, yRight_mc);
    ctx.strokeStyle = '#00e5ff';
    ctx.lineWidth = 3.2;
    ctx.shadowColor = '#fff';
    ctx.shadowBlur = 8;
    ctx.globalAlpha = 0.98;
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.globalAlpha = 1;
    ctx.restore();
  }
  // Tick en V pour chaque planète
  for (const planete in json.planetes) {
    const deg = json.planetes[planete];
    const angleRad = Math.PI - (deg / 360) * 2 * Math.PI;
    let vLen = vSize;
    const xV = cx + rV * Math.cos(angleRad);
    const yV = cy + rV * Math.sin(angleRad);
    const angleLeft = angleRad - Math.PI / 36;
    const angleRight = angleRad + Math.PI / 36;
    const xLeft = xV + vLen * Math.cos(angleLeft);
    const yLeft = yV + vLen * Math.sin(angleLeft);
    const xRight = xV + vLen * Math.cos(angleRight);
    const yRight = yV + vLen * Math.sin(angleRight);
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(xLeft, yLeft);
    ctx.lineTo(xV, yV);
    ctx.lineTo(xRight, yRight);
    ctx.strokeStyle = '#ffe066';
    ctx.lineWidth = 3.2;
    ctx.shadowColor = '#fff';
    ctx.shadowBlur = 8;
    ctx.globalAlpha = 0.98;
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.globalAlpha = 1;
    ctx.restore();
  }
  // Affichage des images des planètes
  const planetesFiles = {
    'Sun': 'sun.png', 'Moon': 'moon.png', 'Mercury': 'mercury.png', 'Venus': 'venus.png',
    'Mars': 'mars.png', 'Jupiter': 'jupiter.png', 'Saturn': 'saturn.png', 'Uranus': 'uranus.png',
    'Neptune': 'neptune.png', 'Pluto': 'pluto.png', 'Chiron': 'chiron.png', 'North Node': 'north-node.png',
    'Part of Fortune': 'part-of-fortune.png'
  };
  const planetesPath = '/static/planetes/';
  const planetRadiusOffset = (typeof json.planetRadiusOffset === 'number') ? json.planetRadiusOffset : 100;
  const baseRadius = radius + planetRadiusOffset; // contrôlable
  for (const planete in json.planetes) {
    const deg = json.planetes[planete];
    const angleRad = Math.PI - (deg / 360) * 2 * Math.PI;
    const x = cx + baseRadius * Math.cos(angleRad);
    const y = cy + baseRadius * Math.sin(angleRad);
    const file = planetesFiles[planete] || null;
    if (file) {
      const img = new window.Image();
      img.src = planetesPath + file;
      img.onload = function() {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(angleRad + Math.PI / 2);
        ctx.beginPath();
        ctx.arc(0, 0, 14, 0, 2 * Math.PI); // plus petit
        ctx.clip();
        ctx.drawImage(img, -14, -14, 28, 28); // plus petit
        ctx.restore();
      };
    } else {
      ctx.save();
      ctx.beginPath();
      ctx.arc(x, y, 18, 0, 2 * Math.PI);
      ctx.fillStyle = '#ffe066';
      ctx.globalAlpha = 0.92;
      ctx.shadowColor = '#6a4fcf';
      ctx.shadowBlur = 8;
      ctx.fill();
      ctx.restore();
    }
  }
}

window.drawRepereASMC = function(themeData, ctx, canvas) {
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const radius = canvas.width / 2 - 180;
  if (themeData) {
    // AS : flèche très visible
    const asDeg = themeData.ascendant;
    const asAngle = Math.PI - (asDeg / 360) * 2 * Math.PI;
    const asR = radius + 60;
    const asX = cx + asR * Math.cos(asAngle);
    const asY = cy + asR * Math.sin(asAngle);
    ctx.save();
    ctx.translate(asX, asY);
    ctx.rotate(asAngle + Math.PI / 2);
    ctx.beginPath();
    ctx.moveTo(0, -28);
    ctx.lineTo(18, 22);
    ctx.lineTo(-18, 22);
    ctx.closePath();
    ctx.fillStyle = '#2979ff';
    ctx.shadowColor = '#fff';
    ctx.shadowBlur = 18;
    ctx.fill();
    ctx.restore();
    // MC : rond très visible
    const mcDeg = themeData.mc;
    const mcAngle = Math.PI - (mcDeg / 360) * 2 * Math.PI;
    const mcR = radius + 60;
    const mcX = cx + mcR * Math.cos(mcAngle);
    const mcY = cy + mcR * Math.sin(mcAngle);
    ctx.save();
    ctx.beginPath();
    ctx.arc(mcX, mcY, 22, 0, 2 * Math.PI);
    ctx.lineWidth = 6;
    ctx.strokeStyle = '#00e5ff';
    ctx.shadowColor = '#fff';
    ctx.shadowBlur = 18;
    ctx.stroke();
    ctx.restore();
  }
}
