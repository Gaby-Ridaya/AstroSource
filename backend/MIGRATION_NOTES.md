# Notes de Migration AstroSource

## Architecture Professionnelle

### Ancien système:
- `fusion_complte.py` - Génération de prompts (ROOT)
- `astro_calcule.py` - Calculs astrologiques (ROOT)
- `nouvelle_roue.py` - Génération SVG (ROOT)

### Nouvelle structure:
- `app/services/prompt_generation.py` - Service de génération de prompts
- `app/services/astro_generation.py` - Service de génération SVG
- `app/services/interpretation.py` - Service d'interprétations
- `app/api/routes/prompt_generation.py` - API de génération de prompts

### Fonctionnalités migrées:
✅ Génération de prompts artistiques IA
✅ Styles poétiques configurables
✅ Fusion données astrologiques + art
✅ API RESTful professionnelle

### Fichiers legacy:
- `scripts/fusion_complte_legacy.py` - Ancienne version pour référence
