# Configuration iOS Shortcuts

## Raccourci "Transcrire YouTube" (version simple)

### Configuration pas à pas

1. **Ouvre l'app Raccourcis** sur iOS

2. **Crée un nouveau raccourci** (+ en haut à droite)

3. **Ajoute ces actions dans l'ordre** :

#### Action 1 : Recevoir l'URL
- Cherche : "Recevoir"
- Sélectionne : "Recevoir [Entrée du raccourci]"
- Configure : "URLs" depuis "Entrée du raccourci"

#### Action 2 : Définir l'URL de l'API
- Cherche : "Texte"
- Entre : `https://TON-SITE.netlify.app/.netlify/functions/youtube-transcript`
- ⚠️ Remplace `TON-SITE` par l'URL de ton site Netlify

#### Action 3 : Créer le JSON
- Cherche : "Dictionnaire"
- Ajoute deux clés :
  * `url` : `[URLs reçues]` (glisse la variable)
  * `languages` : `["fr", "en"]` (texte)

#### Action 4 : Appeler l'API
- Cherche : "Obtenir le contenu de l'URL"
- URL : `[Texte]` (glisse la variable de l'Action 2)
- Méthode : **POST**
- En-têtes : Ajoute `Content-Type` = `application/json`
- Corps de la requête : **JSON** → `[Dictionnaire]` (glisse la variable de l'Action 3)

#### Action 5 : Parser la réponse
- Cherche : "Obtenir le dictionnaire depuis"
- Sélectionne : `[Contenu de l'URL]`

#### Action 6 : Extraire le markdown
- Cherche : "Obtenir la valeur du dictionnaire"
- Clé : `markdown`
- Dictionnaire : `[Dictionnaire]` (de l'Action 5)

#### Action 7 : Afficher ou copier
Choisis l'une de ces options :

**Option A : Copier dans le presse-papiers**
- Cherche : "Copier dans le presse-papiers"
- Contenu : `[Valeur du dictionnaire]`
- Puis ajoute : "Afficher la notification" → "✅ Transcription copiée"

**Option B : Affichage rapide**
- Cherche : "Affichage rapide"
- Contenu : `[Valeur du dictionnaire]`

**Option C : Menu de choix**
- Cherche : "Choisir parmi les options"
- Options :
  * "Copier" → Copier dans le presse-papiers
  * "Afficher" → Affichage rapide
  * "Partager" → Partager

4. **Configure le partage**
   - Appuie sur l'icône ⓘ (en bas à droite)
   - Active : "Afficher dans la feuille de partage"
   - Types acceptés : "URLs"

5. **Nomme ton raccourci**
   - En haut : "Transcrire YouTube"
   - Icône : 🎬 ou 📝

6. **Teste !**
   - Ouvre YouTube
   - Choisis une vidéo avec sous-titres
   - Appuie sur Partager
   - Sélectionne ton raccourci
   - Attends 5-10 secondes
   - La transcription apparaît !

## Structure visuelle du raccourci

```
┌─────────────────────────────────┐
│ Recevoir URLs                   │
│ depuis Entrée du raccourci      │
├─────────────────────────────────┤
│ Texte:                          │
│ https://ton-site.netlify.app/...│
├─────────────────────────────────┤
│ Dictionnaire:                   │
│ • url: [URLs reçues]            │
│ • languages: ["fr", "en"]       │
├─────────────────────────────────┤
│ Obtenir le contenu de [Texte]  │
│ POST + JSON                     │
├─────────────────────────────────┤
│ Obtenir dictionnaire            │
├─────────────────────────────────┤
│ Obtenir valeur "markdown"       │
├─────────────────────────────────┤
│ Copier / Afficher / Partager    │
└─────────────────────────────────┘
```

## Variante : Créer directement un document Craft

Après l'Action 6 (obtenir markdown) :

```
7. Obtenir valeur "video_id" du dictionnaire

8. Texte : "Transcription YouTube - [video_id]"

9. Ouvrir URL : craftdocs://createdocument?title=[Texte]&content=[markdown]
```

*(Note : Cette URL scheme fonctionne si Craft est installé)*

## Dépannage

**Le raccourci ne s'affiche pas dans le menu Partager**
→ Vérifie que "Afficher dans la feuille de partage" est activé
→ Vérifie que "URLs" est accepté

**Erreur "Impossible de se connecter"**
→ Vérifie l'URL Netlify (doit contenir `/.netlify/functions/`)
→ Vérifie ta connexion internet

**Erreur "Aucune transcription disponible"**
→ La vidéo doit avoir des sous-titres
→ Essaie avec une autre vidéo (ou langue différente)

**Le raccourci prend trop de temps**
→ Vidéo peut-être trop longue
→ Attends jusqu'à 30 secondes max
→ Si ça timeout, la vidéo est trop longue

## Astuces

### Ajouter à l'écran d'accueil
1. Ouvre le raccourci
2. Icône ⓘ → Ajouter à l'écran d'accueil
3. Personnalise nom et icône

### Widget Raccourcis
1. Long-press sur l'écran d'accueil
2. Ajoute widget "Raccourcis"
3. Choisis ton raccourci

### Siri
Tu peux aussi invoquer le raccourci avec Siri :
"Hey Siri, Transcrire YouTube"
