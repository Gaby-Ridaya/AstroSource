// Module : Dessin des maisons astrologiques, AS et MC
// Utilisation : drawMaisons(ctx, params)

window.drawMaisons = function(ctx, params) {
  // ctx : contexte canvas
  // params : {cx, cy, radius, maisons_deg, ascendant, mc}
  const { cx, cy, radius, maisons_deg, ascendant, mc } = params;
  if (!maisons_deg || !Array.isArray(maisons_deg)) return;
  // Suppression du dessin des traits des maisons (on garde uniquement les numéros)
  // Affichage des numéros des maisons au centre de chaque secteur
  ctx.save();
  ctx.font = 'bold 16px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = '#fff';
  const radiusNum = radius + 0.50; // bien entre les deux cercles

  // Dessine un cercle juste au-dessus des numéros
  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, radiusNum + 12, 0, 2 * Math.PI);
  ctx.strokeStyle = '#fff';
  ctx.lineWidth = 2.5;
  ctx.globalAlpha = 0.7;
  ctx.shadowColor = '#2979ff';
  ctx.shadowBlur = 6;
  ctx.stroke();
  ctx.restore();
  for (let i = 0; i < maisons_deg.length; i++) {
    // Angle au centre du secteur maison
    const degStart = maisons_deg[i];
    const degEnd = maisons_deg[(i + 1) % maisons_deg.length];
    let degCenter = degStart + (((degEnd - degStart + 360) % 360) / 2);
    if (degCenter >= 360) degCenter -= 360;
    const angleNum = Math.PI - (degCenter / 360) * 2 * Math.PI;
    const xNum = cx + radiusNum * Math.cos(angleNum);
    const yNum = cy + radiusNum * Math.sin(angleNum);
    ctx.fillText((i + 1).toString(), xNum, yNum);
  }
  ctx.restore();

  // Les flèches des cuspides sont supprimées comme demandé
  // Dessin de l'Ascendant (AS)
  if (typeof ascendant === 'number') {
    const angleAS = Math.PI - (ascendant / 360) * 2 * Math.PI;
    const xAS = cx + (radius + 18) * Math.cos(angleAS);
    const yAS = cy + (radius + 18) * Math.sin(angleAS);
    ctx.save();
    ctx.beginPath();
    ctx.arc(xAS, yAS, 14, 0, 2 * Math.PI);
    ctx.fillStyle = '#a020f0'; // violet
    ctx.globalAlpha = 1.0;
    ctx.shadowColor = '#a020f0';
    ctx.shadowBlur = 14;
    ctx.fill();
    ctx.restore();
    // Texte A blanc au centre
    ctx.save();
    ctx.font = 'bold 18px Arial';
    ctx.fillStyle = '#fff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('A', xAS, yAS);
    ctx.restore();
  }
  // Dessin du Milieu du Ciel (MC)
  if (typeof mc === 'number') {
    const angleMC = Math.PI - (mc / 360) * 2 * Math.PI;
    const xMC = cx + (radius + 18) * Math.cos(angleMC);
    const yMC = cy + (radius + 18) * Math.sin(angleMC);
    ctx.save();
    ctx.beginPath();
    ctx.arc(xMC, yMC, 14, 0, 2 * Math.PI);
    ctx.fillStyle = '#ff7300ff'; // turquoise
    ctx.globalAlpha = 1.0;
    ctx.shadowColor = '#ff800031';
    ctx.shadowBlur = 14;
    ctx.fill();
    ctx.restore();
    // Texte M blanc au centre
    ctx.save();
    ctx.font = 'bold 18px Arial';
    ctx.fillStyle = '#fff';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('M', xMC, yMC);
    ctx.restore();
  }
}
