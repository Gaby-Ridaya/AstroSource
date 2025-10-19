// JS pour validation et soumission AJAX du formulaire astrologique

document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('.art-astro-form, .astro-form');
  const resultDiv = document.querySelector('.art-astro-result');

  if (!form) return;

  // Validation simple avant envoi
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    let valid = true;
    let fields = ['nom', 'date', 'heure', 'ville', 'pays'];
    fields.forEach(function(id) {
      const input = document.getElementById(id);
      if (!input.value.trim()) {
        input.style.borderColor = '#00eaff'; // turquoise astral pour l'erreur
        valid = false;
      } else {
        input.style.borderColor = '#4fc3ff';
      }
    });
    if (!valid) return;

    // Envoi AJAX
    const formData = new FormData(form);
    fetch(form.action, {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(html => {
      // Affiche le résultat dans le bloc prévu
      if (resultDiv) {
        resultDiv.innerHTML = html;
      } else {
        // Si pas de bloc, affiche en popup
        alert('Résultat : ' + html);
      }
    })
    .catch(() => {
      alert('Erreur lors de la génération.');
    });
  });
});
