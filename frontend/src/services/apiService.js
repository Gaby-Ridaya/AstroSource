// src/services/apiService.js
const API_BASE = "http://127.0.0.1:8000"; // adapte si besoin

export const apiService = {
  // 1) Génère le SVG via ton endpoint existant (tu l'utilises déjà)
  async generateTheme(payload) {
    const resp = await fetch(`${API_BASE}/api/generer-svg`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!resp.ok) {
      const text = await resp.text().catch(() => "");
      throw new Error(`Erreur SVG (${resp.status}) ${text}`);
    }
    // L’API renvoie le SVG inline (string)
    return resp.text();
  },

  // 2) Déclenche la génération IMAGE/INTERPS/ZIP côté backend
  //    et renvoie aussi des URLs de téléchargement prêtes pour le frontend.
  async prepareDownloads(username) {
    const url = `${API_BASE}/api/astro-image/${encodeURIComponent(username)}`;
    const resp = await fetch(url);
    if (!resp.ok) {
      const text = await resp.text().catch(() => "");
      throw new Error(`Erreur image/pack (${resp.status}) ${text}`);
    }
    const data = await resp.json();

    // Construit des liens propres vers la route de download
    const downloads = {
      pack: `${API_BASE}/api/download/${encodeURIComponent(username)}/pack`,
      image: `${API_BASE}/api/download/${encodeURIComponent(username)}/image`,
      interpretations: `${API_BASE}/api/download/${encodeURIComponent(username)}/interpretations`,
      pdf: `${API_BASE}/api/download/${encodeURIComponent(username)}/pdf`, // <--- nouveau
      svg: `${API_BASE}/api/download/${encodeURIComponent(username)}/svg`,
    };

    return { ...data, downloads };
  },

  // 3) (Optionnel) Si tu veux juste l’URL directe de l’image
  async getAstroImage(username) {
    const r = await this.prepareDownloads(username);
    return r.downloads.image; // compat avec ton ancien code si besoin
  },
};
