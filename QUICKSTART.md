# 🚀 Démarrage en 5 minutes

## Étape 1 : Test local (optionnel - 2 min)

```bash
# Installe la dépendance
pip install youtube-transcript-api

# Teste avec une vidéo (exemple : Never Gonna Give You Up)
python test_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Un fichier transcript_dQw4w9WgXcQ.md sera créé
# Ouvre-le pour voir le résultat !
```

## Étape 2 : Déploie sur Netlify (3 min)

### Option A : Via l'interface web (recommandé)

1. Va sur https://app.netlify.com
2. Clique "Add new site" → "Import an existing project"
3. Connecte ton repo GitHub/GitLab avec ces fichiers
4. Clique "Deploy site"
5. Attends 1-2 minutes
6. Note ton URL : `https://ton-site-123456.netlify.app`

### Option B : Via CLI

```bash
# Installe Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Initialise et déploie
netlify init
netlify deploy --prod

# Note l'URL affichée
```

## Étape 3 : Configure iOS Shortcuts (5 min)

1. Ouvre l'app **Raccourcis** sur iOS
2. Crée un nouveau raccourci (+)
3. Ajoute les actions suivantes :

```
Recevoir URLs → Entrée du raccourci
   ↓
Texte → https://TON-SITE.netlify.app/.netlify/functions/youtube-transcript
   ↓
Dictionnaire → {url: [URLs], languages: ["fr","en"]}
   ↓
Obtenir contenu URL → POST + JSON
   ↓
Obtenir dictionnaire
   ↓
Obtenir valeur "markdown"
   ↓
Copier dans presse-papiers + Notification
```

4. Active "Afficher dans la feuille de partage"
5. Sauvegarde : "Transcrire YouTube"

→ **Guide détaillé : [iOS_SHORTCUTS.md](iOS_SHORTCUTS.md)**

## Étape 4 : Teste ! (30 secondes)

1. Ouvre YouTube sur ton iPhone
2. Trouve une vidéo avec sous-titres (exemple : TED Talk)
3. Appuie sur **Partager**
4. Choisis **"Transcrire YouTube"**
5. Attends 5-10 secondes
6. ✅ La transcription est copiée !
7. Colle dans Notes ou Craft

## ✅ C'est tout !

Tu as maintenant un workflow complet pour extraire des transcriptions YouTube.

## 🎯 Prochaines étapes

- Personnalise le format de sortie (voir README.md)
- Crée des variantes du raccourci (voir iOS_SHORTCUTS.md)
- Intègre avec Craft pour créer des documents automatiquement

## 🆘 Besoin d'aide ?

- **Le test local échoue** : Vérifie que youtube-transcript-api est installé
- **Netlify échoue** : Check les logs dans Dashboard → Deploys
- **iOS Shortcuts ne marche pas** : Vérifie l'URL de l'API
- **Pas de transcription** : La vidéo doit avoir des sous-titres

→ Consulte README.md pour plus de détails
