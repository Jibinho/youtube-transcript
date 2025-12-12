# YouTube Transcript - Version Simple

Extraction de transcriptions YouTube avec timestamps cliquables, **sans services payants**.

## 🎯 Fonctionnalités

- ✅ Extraction de transcriptions YouTube (officielles ou auto-générées)
- ✅ Support multi-langues (français, anglais, etc.)
- ✅ Timestamps cliquables pour navigation vidéo
- ✅ Format markdown simple et lisible
- ✅ 100% gratuit (pas de Claude API, pas d'autres services payants)
- ✅ Compatible iOS Shortcuts

## 📋 Exemple de sortie

```markdown
# Transcription YouTube

**Vidéo** : https://www.youtube.com/watch?v=dQw4w9WgXcQ
**Langue** : en
**Segments** : 234

---

[⏱️ 00:00](https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=0s) We're no strangers to love

[⏱️ 00:03](https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=3s) You know the rules and so do I

[⏱️ 00:06](https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=6s) A full commitment's what I'm thinking of

...
```

Chaque ligne contient :
- Un timestamp cliquable (ouvre YouTube au moment exact)
- Le texte correspondant du sous-titre

**Tu peux ensuite nettoyer et structurer ce contenu comme tu veux !**

## 🚀 Installation rapide (5 minutes)

### 1. Déploie sur Netlify

```bash
# Option A : Via GitHub
1. Crée un repo avec ces fichiers
2. Connecte-le à Netlify
3. Déploie !

# Option B : Via Netlify CLI
netlify login
netlify init
netlify deploy --prod
```

### 2. Configure iOS Shortcuts

Dans l'app Raccourcis iOS :

```
1. Recevoir : URLs depuis Entrée du raccourci

2. Obtenir le contenu de l'URL
   - URL : https://ton-site.netlify.app/.netlify/functions/youtube-transcript
   - Méthode : POST
   - Headers : Content-Type: application/json
   - Body : {"url": "[URLs reçues]", "languages": ["fr", "en"]}

3. Obtenir le dictionnaire depuis : Contenu de l'URL

4. Obtenir la valeur "markdown" du dictionnaire

5. Copier dans le presse-papiers / Afficher / Partager
```

Active "Afficher dans la feuille de partage" pour utiliser depuis YouTube.

## 🧪 Test local

```bash
# Installe la dépendance
pip install youtube-transcript-api

# Teste avec une vidéo
python test_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Le fichier transcript_VIDEO_ID.md sera créé
```

## 📡 API

### Endpoint
```
POST https://ton-site.netlify.app/.netlify/functions/youtube-transcript
```

### Requête
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "languages": ["fr", "en"]
}
```

### Réponse (200)
```json
{
  "success": true,
  "video_id": "VIDEO_ID",
  "language": "fr",
  "is_generated": false,
  "segments_count": 234,
  "markdown": "# Transcription YouTube\n\n..."
}
```

## 💰 Coûts

**Totalement gratuit !**
- Netlify : Plan gratuit (125 000 requêtes/mois)
- YouTube Transcript API : Gratuit
- Pas de clé API nécessaire
- Pas de services payants

## 🔧 Personnalisation

### Modifier les langues préférées

Dans `functions/youtube-transcript.py`, ligne 72 :
```python
languages = body.get('languages', ['fr', 'en', 'es'])
```

### Changer le format de sortie

Modifie la fonction `format_transcript_to_markdown()` pour :
- Grouper plusieurs segments
- Ajouter des paragraphes
- Changer le style des timestamps
- Etc.

## 📝 Après extraction

Une fois la transcription extraite, tu peux la nettoyer et structurer :
- Avec un éditeur de texte
- Avec des scripts de traitement
- Avec Claude Desktop (en local, gratuit)
- Manuellement selon tes besoins

## ⚠️ Limitations

- Vidéo doit avoir des sous-titres disponibles
- Pas de structuration automatique (markdown brut)
- Timeout Netlify : 10 secondes (gratuit) ou 26 secondes (payant)

## 📚 Structure du projet

```
youtube-transcript-simple/
├── functions/
│   └── youtube-transcript.py    # Fonction principale
├── netlify.toml                 # Config Netlify
├── requirements.txt             # Dépendances
├── test_transcript.py          # Test local
└── README.md                   # Documentation
```

## 🎉 Utilisation

1. Trouve une vidéo YouTube avec sous-titres
2. Partage → Ton raccourci iOS
3. La transcription brute avec timestamps apparaît
4. Copie/Colle dans ton éditeur préféré
5. Nettoie et structure comme tu veux !

## 📄 Licence

MIT - Utilise librement
