import React, { useState } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState("");
  const [cms, setCms] = useState("auto");
  const [goal, setGoal] = useState("vente");
  const [tone, setTone] = useState("professionnel");
  const [loading, setLoading] = useState(false);
  const [original, setOriginal] = useState("");
  const [suggestion, setSuggestion] = useState("");
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!url.trim()) {
      alert("Merci d'entrer une URL valide.");
      return;
    }

    setLoading(true);
    setOriginal("");
    setSuggestion("");
    setError("");

    try {
      const response = await fetch("https://autowebai-api.onrender.com/analyze-url", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url, cms, goal, tone }), // 🆕 envoi des nouvelles options
      });

      const data = await response.json();

      console.log("Réponse de l'API :", data);

      if (data.error) {
        setError(data.error);
      } else {
        setOriginal(data.original);
        setSuggestion(data.suggestion);
      }
    } catch (err) {
      console.error("Erreur lors de la requête vers l'API :", err);
      setError("Une erreur est survenue lors de la connexion à l'IA.");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (suggestion) {
      navigator.clipboard.writeText(suggestion)
        .then(() => alert("Contenu copié dans le presse-papiers"))
        .catch(() => alert("Erreur lors de la copie"));
    }
  };

  const handleEmail = () => {
    if (suggestion) {
      const subject = encodeURIComponent("Suggestion IA pour votre site");
      const body = encodeURIComponent(suggestion);
      window.location.href = `mailto:?subject=${subject}&body=${body}`;
    }
  };

  const handleApplyCMS = () => {
    alert("Fonctionnalité bientôt disponible 😉");
  };

  return (
    <div className="App">
      <h1>Bienvenue sur AutoWebAI</h1>
      <p>Entrez l'URL de votre site pour générer une version optimisée par IA :</p>

      {/* Sélecteur de CMS */}
      <div style={{ marginBottom: "10px" }}>
        <label>
          CMS :
          <select
            value={cms}
            onChange={(e) => setCms(e.target.value)}
            style={{ marginLeft: "10px", padding: "6px", fontSize: "16px" }}
          >
            <option value="auto">Détection automatique</option>
            <option value="wordpress">WordPress</option>
            <option value="shopify">Shopify</option>
            <option value="wix">Wix</option>
            <option value="webflow">Webflow</option>
            <option value="autre">Autre</option>
          </select>
        </label>
      </div>

      {/* Sélecteur d'objectif */}
      <div style={{ marginBottom: "10px" }}>
        <label>
          Objectif :
          <select
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            style={{ marginLeft: "10px", padding: "6px", fontSize: "16px" }}
          >
            <option value="vente">Vendre un produit</option>
            <option value="lead">Obtenir des contacts (leads)</option>
            <option value="blog">Partager des infos / articles</option>
            <option value="portfolio">Montrer un projet / CV</option>
          </select>
        </label>
      </div>

      {/* Sélecteur de ton */}
      <div style={{ marginBottom: "15px" }}>
        <label>
          Ton souhaité :
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            style={{ marginLeft: "10px", padding: "6px", fontSize: "16px" }}
          >
            <option value="professionnel">Professionnel</option>
            <option value="convivial">Convivial</option>
            <option value="persuasif">Persuasif</option>
            <option value="créatif">Créatif</option>
          </select>
        </label>
      </div>

      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://exemple.com"
        style={{ width: "60%", padding: "10px", fontSize: "16px" }}
      />
      <br />
      <button className="cta" onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyse en cours..." : "Analyser le site"}
      </button>

      {error && (
        <div style={{ color: "red", marginTop: "20px" }}>
          <strong>Erreur :</strong> {error}
        </div>
      )}

      {original && (
        <div className="result">
          <h2>Contenu extrait :</h2>
          <p>{original}</p>
        </div>
      )}

      {suggestion && (
        <div className="result">
          <h2>Suggestion IA :</h2>
          <p>{suggestion}</p>
          <div style={{ marginTop: "15px" }}>
            <button onClick={handleCopy} style={{ marginRight: "10px" }}>
              ✅ Copier
            </button>
            <button onClick={handleEmail} style={{ marginRight: "10px" }}>
              📧 Envoyer par email
            </button>
            <button onClick={handleApplyCMS}>
              🔧 Appliquer au CMS
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
