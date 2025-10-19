// Module : Affichage du tableau résumé du thème astrologique
// Utilisation : import et appel showThemeSummary(themeData)

export function showThemeSummary(themeData) {
  const themeSummary = document.getElementById('themeSummary');
  if (!themeSummary || !themeData) return;
  document.getElementById('themeDate').textContent = themeData.date || '...';
  document.getElementById('themePlace').textContent = themeData.lieu || '...';
  document.getElementById('themeLon').textContent = themeData.longitude || '...';
  document.getElementById('themeLat').textContent = themeData.latitude || '...';
  // Tableau des planètes
  const planetsTable = document.getElementById('planetsTable');
  if (planetsTable) {
    let html = '<table style="width:100%;border-collapse:collapse;font-size:0.97em;">';
    html += '<tr><th style="color:#ffe066;font-weight:600;text-align:left;padding-bottom:6px;">Planète</th><th style="color:#ffe066;font-weight:600;text-align:left;padding-bottom:6px;">Position</th></tr>';
    const planetNames = ['sun','moon','mercury','venus','mars','jupiter','saturn','uranus','neptune','pluto','chiron','north-node'];
    const planetLabels = ['Soleil','Lune','Mercure','Vénus','Mars','Jupiter','Saturne','Uranus','Neptune','Pluton','Chiron','Noeud Nord'];
    const planetKeys = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto','Chiron','North Node'];
    const signNames = ['aries','taurus','gemini','cancer','leo','virgo','libra','scorpio','sagittarius','capricorn','aquarius','pisces'];
    const signLabels = ['Bélier','Taureau','Gémeaux','Cancer','Lion','Vierge','Balance','Scorpion','Sagittaire','Capricorne','Verseau','Poissons'];
    for (let i = 0; i < planetKeys.length; i++) {
      const key = planetKeys[i];
      const deg = themeData.planetes && themeData.planetes[key];
      let signIdx = -1;
      if (typeof deg === 'number') signIdx = Math.floor(deg / 30);
      html += '<tr>';
      html += `<td style="padding:2px 0;"><img src="/static/planetes_mini/${planetNames[i]}.png" style="width:22px;vertical-align:middle;margin-right:6px;">${planetLabels[i]}</td>`;
      if (signIdx >= 0) {
        html += `<td style="padding:2px 0;"><span style="font-weight:600;color:#ffe066;">${Math.round(deg)}°</span> <img src="/static/signes/${signNames[signIdx]}.png" style="width:18px;vertical-align:middle;margin-left:4px;"> <span style="color:#fff;">${signLabels[signIdx]}</span></td>`;
      } else {
        html += `<td style="padding:2px 0;">...</td>`;
      }
      html += '</tr>';
    }
    html += '</table>';
    planetsTable.innerHTML = html;
  }
}
