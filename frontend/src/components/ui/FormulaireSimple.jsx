import { useState } from "react";
import { apiService } from "../../services/apiService";
import "./FormulaireSimple.css";

function FormulaireSimple() {
  const [nom, setNom] = useState("");
  const [ville, setVille] = useState("");
  const [date, setDate] = useState("");
  const [heure, setHeure] = useState("");

  const [svgContent, setSvgContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [aiImageUrl, setAiImageUrl] = useState("");
  const [loadingImage, setLoadingImage] = useState(false);

  const [downloads, setDownloads] = useState(null); // { pack, image, interpretations, svg }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setDownloads(null);
    setAiImageUrl("");
    try {
      const svgData = await apiService.generateTheme({
        nom: nom,
        ville_naissance: ville,
        date_naissance: date,
        heure_naissance: heure,
      });

      // Petit nettoyage du SVG
      let svgClean = svgData.replace(/data-timestamp="[^"]*"/g, "");
      if (!svgClean.includes("viewBox")) {
        svgClean = svgClean.replace("<svg", '<svg viewBox="0 0 1800 1200"');
      }
      setSvgContent(svgClean);
    } catch (err) {
      setError("Erreur: " + (err.message || "inconnue"));
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAIImage = async () => {
    setLoadingImage(true);
    setError("");
    setAiImageUrl("");
    setDownloads(null);
    try {
      // Déclenche côté backend la génération image + interprétations + zip
      const res = await apiService.prepareDownloads(nom.trim());
      // URL directe de l'image (si tu veux afficher un aperçu)
      setAiImageUrl(res.downloads.image);
      // URLs de téléchargement
      setDownloads(res.downloads);
    } catch (err) {
      setError("Erreur image/pack: " + (err.message || "inconnue"));
    } finally {
      setLoadingImage(false);
    }
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <div className="left-panel">
          <h1>🌟 Générateur de Thème Astral</h1>
          <form onSubmit={handleSubmit}>
            <div>
              <label>Nom:</label>
              <input
                type="text"
                value={nom}
                onChange={(e) => setNom(e.target.value)}
                required
                placeholder="Votre nom (ex: jos.6)"
              />
            </div>

            <div>
              <label>Ville de naissance:</label>
              <input
                type="text"
                value={ville}
                onChange={(e) => setVille(e.target.value)}
                required
                placeholder="Paris, France"
              />
            </div>

            <div>
              <label>Date de naissance:</label>
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
              />
            </div>

            <div>
              <label>Heure de naissance:</label>
              <input
                type="time"
                value={heure}
                onChange={(e) => setHeure(e.target.value)}
                required
              />
            </div>

            <button type="submit" disabled={loading}>
              {loading ? "GÉNÉRATION..." : "GÉNÉRER MON THÈME (SVG)"}
            </button>
          </form>

          {error && <div style={{ color: "red", marginTop: 12 }}>{error}</div>}
        </div>

        <div className="right-panel">
          {svgContent ? (
            <div>
              <h3>🎨 VOTRE CARTE DU CIEL</h3>
              <div
                className="svg-display"
                style={{
                  width: "100%",
                  height: "auto",
                  maxHeight: "700px",
                  background: "white",
                  borderRadius: "8px",
                  overflow: "auto",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <div
                  dangerouslySetInnerHTML={{ __html: svgContent }}
                  style={{ width: "100%", height: "auto", maxWidth: "100%" }}
                />
              </div>

              <button
                style={{
                  marginTop: 24,
                  padding: "12px 24px",
                  fontSize: "1.1em",
                  background: "#00bcd4",
                  color: "white",
                  border: "none",
                  borderRadius: 8,
                  cursor: "pointer",
                  fontWeight: 600,
                }}
                onClick={handleGenerateAIImage}
                disabled={loadingImage || !nom.trim()}
              >
                {loadingImage
                  ? "Génération de l'image & du pack..."
                  : "✨ Générer l’image + interprétations + pack"}
              </button>

              {/* Aperçu image si dispo */}
              {aiImageUrl && (
                <div style={{ marginTop: 24 }}>
                  <h3>🖼️ VOTRE IMAGE ARTISTIQUE</h3>
                  <img
                    src={aiImageUrl}
                    alt="Image AI astrologique"
                    style={{
                      maxWidth: "100%",
                      borderRadius: 12,
                      boxShadow: "0 4px 24px #00bcd488",
                    }}
                  />
                </div>
              )}

              {/* Boutons de téléchargement */}
              {downloads && (
                <div style={{ marginTop: 24 }}>
                  <h3>⬇️ Téléchargements</h3>
                  <div className="button-group">
                    <a className="submit-button" href={downloads.pack}>
                      📦 Télécharger le pack (.zip)
                    </a>
                    <a className="submit-button" href={downloads.image}>
                      🖼️ Télécharger l’image (PNG)
                    </a>
                    <a className="submit-button" href={downloads.interpretations}>
                      📜 Télécharger les interprétations (.txt)
                    </a>
                    <a className="submit-button" href={downloads.pdf}>
                      📄 Télécharger les interprétations (PDF) {/* <--- nouveau */}
                    </a>
                  </div>
                  <div className="button-group" style={{ marginTop: "0.75rem" }}>
                    <a className="clear-button" href={downloads.svg}>
                      🗺️ Télécharger le SVG (roue)
                    </a>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div>
              <h3>🌙 En attente...</h3>
              <p>Remplissez le formulaire pour voir votre thème astral</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default FormulaireSimple;
