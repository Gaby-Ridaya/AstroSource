# README — Fonctionnement du système ART Astro

## Structure générale

- **HTML** : `/templates/art_astro.html`
  - Contient le formulaire astrologique et l’image de la roue zodiacale.
  - Utilise la classe `astro-form` pour le formulaire et `art-astro-btn` pour le bouton.
  - Les champs du formulaire ont les IDs : `nom`, `date`, `heure`, `ville`, `pays`.
  - Le résultat s’affiche dans le bloc `.art-astro-result`.
  - Le JS est inclus via `<script src="/static/js/art_astro_form.js"></script>`.

- **CSS** :
  - `/static/css/roue_form.css` : Styles spécifiques au formulaire et à la roue.
    - Positionnement, transparence, couleurs turquoise, bouton petit et stylé.
    - Sélecteur `.astro-form .art-astro-btn` pour forcer le style du bouton.
  - `/static/css/buttons.css` : Styles globaux pour tous les boutons du site.
    - Peut être surchargé par `roue_form.css` pour le bouton astrologique.

- **JS** : `/static/js/art_astro_form.js`
  - Validation des champs avant envoi (bordure turquoise astral si erreur).
  - Soumission AJAX du formulaire, affichage du résultat dans `.art-astro-result`.
  - Gère l’absence du formulaire pour éviter les erreurs JS.

## Fonctionnement détaillé

1. **Affichage** :
   - La page affiche la roue zodiacale et le formulaire à gauche.
   - Le formulaire est transparent, aligné, et le bouton est turquoise, petit, avec un dégradé.

2. **Validation JS** :
   - À la soumission, chaque champ est vérifié.
   - Si un champ est vide, sa bordure devient turquoise astral (`#00eaff`).
   - Si tout est OK, le formulaire est envoyé en AJAX.

3. **Soumission AJAX** :
   - Les données sont envoyées à `/art_astro` (route Flask).
   - Le résultat (HTML) est affiché dans `.art-astro-result` ou en popup si le bloc n’existe pas.

4. **CSS** :
   - Le style du bouton est forcé par `.astro-form .art-astro-btn` avec `!important`.
   - Les champs sont turquoise, le fond du formulaire est transparent.
   - Les autres boutons du site utilisent `buttons.css`.

## À vérifier / À faire

- [x] Le bouton du formulaire a bien la classe `art-astro-btn` dans le HTML.
- [x] Le fichier `roue_form.css` est chargé après `buttons.css` pour surcharger le style.
- [x] Les IDs des champs du formulaire sont corrects.
- [x] Le JS est bien inclus et fonctionne (validation + AJAX).
- [x] Le backend Flask accepte la route `/art_astro` et retourne un résultat HTML.
- [x] Les erreurs CSS (accolades superflues) ont été corrigées.
- [ ] Tester sur plusieurs navigateurs et vider le cache si besoin.
- [ ] Ajouter des messages d’erreur plus explicites côté JS si nécessaire.
- [ ] Améliorer l’accessibilité (labels, contrastes, focus).
- [ ] Ajouter une animation de chargement lors de la génération de l’image.

## Bonnes pratiques
- Utiliser des classes CSS spécifiques pour éviter les conflits.
- Toujours vérifier l’inclusion des fichiers JS/CSS dans le template.
- Utiliser `!important` uniquement pour forcer un style en cas de conflit.
- Tester la validation et l’envoi du formulaire sur différents navigateurs.

---

Pour toute modification, suivre la structure ci-dessus et tester chaque étape (affichage, validation, soumission, résultat).
