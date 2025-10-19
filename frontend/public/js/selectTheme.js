// Module : Sélecteur de thèmes astrologiques
// Affiche la liste des thèmes et recharge la roue au clic

export async function afficherThemes(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = '<div style="color:#9ddfff;font-weight:bold;margin-bottom:8px;">Thèmes disponibles :</div>';
  try {
    const response = await fetch('/api/themes');
    if (!response.ok) throw new Error('Erreur API');
    const themes = await response.json();
    if (!themes.length) {
      container.innerHTML += '<div style="color:#ffe066;">Aucun thème trouvé.</div>';
      return;
    }
    const ul = document.createElement('ul');
    ul.style.listStyle = 'none';
    ul.style.padding = '0';
    themes.forEach(theme => {
      const li = document.createElement('li');
      li.style.marginBottom = '6px';
      const a = document.createElement('a');
      a.textContent = theme.name;
      a.href = `?theme_id=${theme.theme_id}`;
      a.style.color = '#66fff7';
      a.style.fontWeight = 'bold';
      a.style.textDecoration = 'none';
      a.style.cursor = 'pointer';
      a.onclick = (e) => {
        e.preventDefault();
        window.location.search = `?theme_id=${theme.theme_id}`;
      };
      li.appendChild(a);
      ul.appendChild(li);
    });
    container.appendChild(ul);
  } catch (err) {
    container.innerHTML += '<div style="color:#ff6666;">Erreur lors du chargement des thèmes.</div>';
  }
}
