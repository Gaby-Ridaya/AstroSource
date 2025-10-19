// Module : Dessin des aspects astrologiques
// Utilisation : drawAspects(ctx, params)

window.drawAspects = function(ctx, params) {
  // ctx : contexte canvas
  // params : {cx, cy, radius, aspects, planetes}
  // Dessine les traits et points pour les aspects
  const { cx, cy, radius, aspects, planetes } = params;
  if (!aspects || !planetes) return;
  for (const aspect of aspects) {
    const [p1, p2] = aspect.planetes.split(' - ');
    const deg1 = planetes[p1];
    const deg2 = planetes[p2];
    if (typeof deg1 !== 'number' || typeof deg2 !== 'number') continue;
    // Les aspects pointent et s'arrêtent sur le premier cercle doré intérieur (radius - 100)
    const rAspectCircle = radius - 100;
    const angle1 = Math.PI - (deg1 / 360) * 2 * Math.PI;
    const angle2 = Math.PI - (deg2 / 360) * 2 * Math.PI;
    const x1 = cx + rAspectCircle * Math.cos(angle1);
    const y1 = cy + rAspectCircle * Math.sin(angle1);
    const x2 = cx + rAspectCircle * Math.cos(angle2);
    const y2 = cy + rAspectCircle * Math.sin(angle2);
    ctx.save();
    if (aspect.aspect === '☌') {
      // Conjonction : petit rond bleu au milieu
      const rAspect = radius - 98 - 22;
      const aspectDeg = (deg1 + aspect.angle) % 360;
      const angleRad = Math.PI - (aspectDeg / 360) * 2 * Math.PI;
      const xA = cx + rAspect * Math.cos(angleRad);
      const yA = cy + rAspect * Math.sin(angleRad);
      ctx.beginPath();
      ctx.arc(xA, yA, 8, 0, 2 * Math.PI);
      ctx.fillStyle = '#2979ff';
      ctx.globalAlpha = 0.95;
      ctx.shadowColor = '#fff';
      ctx.shadowBlur = 8;
      ctx.fill();
    } else {
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      // Couleur et style selon l'aspect
      if (aspect.aspect === '□') {
        ctx.setLineDash([6, 6]);
        ctx.strokeStyle = '#ffb3b3'; // rouge pastel
        ctx.lineWidth = 2.2;
      } else if (aspect.aspect === '△') {
        ctx.strokeStyle = '#a3c9ff'; // bleu pastel
        ctx.lineWidth = 2.2;
      } else if (aspect.aspect === '✶') {
        ctx.strokeStyle = '#b2f2d0'; // vert pastel
        ctx.lineWidth = 2.2;
      } else if (aspect.aspect === '☍') {
        ctx.strokeStyle = '#e1b3ff'; // violet pastel
        ctx.lineWidth = 2.2;
      } else {
        ctx.strokeStyle = '#f5f5f5'; // blanc doux
        ctx.lineWidth = 1.7;
      }
      ctx.globalAlpha = 0.65;
      ctx.shadowColor = '#fff';
      ctx.shadowBlur = 5;
      ctx.stroke();
      ctx.setLineDash([]);
    }
    ctx.restore();
  }
}
