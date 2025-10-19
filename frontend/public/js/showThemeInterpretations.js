// showThemeInterpretations.js
// Module dynamique pour afficher les interprétations d'un thème astrologique
// Exemple d'utilisation :
// showThemeInterpretations({ house: 'Maison_1', planet: 'Mars', dignity: 'dignite_Mars' });

// Fonction utilitaire pour charger les interprétations
async function fetchInterpretations() {
  const housesPromise = fetch('/static/interpretations_json/houses.json').then(r => r.json());
  const planetsPromise = fetch('/static/interpretations_json/planets.json').then(r => r.json());
  const dignitiesPromise = fetch('/static/interpretations_json/dignities.json').then(r => r.json());
  const [houses, planets, dignities] = await Promise.all([housesPromise, planetsPromise, dignitiesPromise]);
  return { houses, planets, dignities };
}

// Affiche dynamiquement les interprétations pour le thème donné
// themeData doit contenir les clés : house, planet, dignity
export async function showThemeInterpretations(themeData) {
  const { houses, planets, dignities } = await fetchInterpretations();

  // Ajout des boutons fixes à droite
  let btns = document.getElementById('themeInterpBtns');
  if (!btns) {
    btns = document.createElement('div');
    btns.id = 'themeInterpBtns';
    btns.style.position = 'fixed';
    btns.style.top = '120px';
    btns.style.right = '24px';
    btns.style.zIndex = '1001';
    btns.innerHTML = `
      <button id='btnShowMaisons' style='display:block;margin-bottom:8px;background:#ffe066;color:#222;border:1px solid #a08000;border-radius:8px;padding:8px 18px;font-size:1em;cursor:pointer;'>Maisons</button>
      <button id='btnShowPlanetes' style='display:block;margin-bottom:8px;background:#ffe066;color:#222;border:1px solid #a08000;border-radius:8px;padding:8px 18px;font-size:1em;cursor:pointer;'>Planètes</button>
      <button id='btnShowDignites' style='display:block;background:#ffe066;color:#222;border:1px solid #a08000;border-radius:8px;padding:8px 18px;font-size:1em;cursor:pointer;'>Dignités</button>
    `;
    document.body.appendChild(btns);
  }

  // Fonction pour ouvrir la fenêtre latérale
  function openSidePanel(contentHtml, title) {
    let panel = document.getElementById('themeInterpPanel');
    if (!panel) {
      panel = document.createElement('div');
      panel.id = 'themeInterpPanel';
      panel.style.position = 'fixed';
      panel.style.top = '0';
      panel.style.right = '0';
      panel.style.width = '420px';
      panel.style.height = '100vh';
      panel.style.background = 'transparent';
      panel.style.color = '#222';
      panel.style.borderLeft = '2px solid #a08000';
      panel.style.boxShadow = '0 0 24px #0004';
      panel.style.zIndex = '1002';
      panel.style.overflowY = 'auto';
      panel.style.padding = '32px 28px 24px 28px';
      panel.style.transition = 'right 0.3s';
      document.body.appendChild(panel);
    }
    panel.innerHTML = `<button id='closeThemeInterpPanel' style='position:absolute;top:18px;right:18px;font-size:1.2em;background:#ffe066;border:none;border-radius:6px;padding:4px 12px;cursor:pointer;'>Fermer</button>
      <h2 style='color:#a08000;text-align:center;margin-bottom:18px;'>${title}</h2>
      ${contentHtml}`;
    document.getElementById('closeThemeInterpPanel').onclick = () => {
      panel.style.right = '-440px';
      setTimeout(() => panel.remove(), 300);
    };
    panel.style.right = '0';
  }

  // Construction des contenus
  let housesHtml = '';
  for (const [key, value] of Object.entries(houses)) {
    housesHtml += `<div style='margin-bottom:10px;'><strong>${key} :</strong><br><span style='font-size:0.97em;'>${value}</span></div>`;
  }
  let planetsHtml = '';
  for (const [key, value] of Object.entries(planets)) {
    planetsHtml += `<div style='margin-bottom:10px;'><strong>${key} :</strong><br><span style='font-size:0.97em;'>${value}</span></div>`;
  }
  let dignitiesHtml = '';
  for (const [key, value] of Object.entries(dignities)) {
    dignitiesHtml += `<div style='margin-bottom:10px;'><strong>${key} :</strong><br><span style='font-size:0.97em;'>${value}</span></div>`;
  }

  // Ajout des listeners sur les boutons
  document.getElementById('btnShowMaisons').onclick = () => openSidePanel(housesHtml, 'Interprétations des maisons');
  document.getElementById('btnShowPlanetes').onclick = () => openSidePanel(planetsHtml, 'Interprétations des planètes');
  document.getElementById('btnShowDignites').onclick = () => openSidePanel(dignitiesHtml, 'Interprétations des dignités');
// ...existing code...
}

// Exemple d'utilisation :
// showThemeInterpretations({ house: 'Maison_1', planet: 'Mars', dignity: 'dignite_Mars' });
