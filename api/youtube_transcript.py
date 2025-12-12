import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from http.server import BaseHTTPRequestHandler


def extract_video_id(url):
    """Extrait l'ID de la vidéo YouTube depuis différents formats d'URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/shorts\/([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def format_timestamp(seconds):
    """Convertit les secondes en format HH:MM:SS ou MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def get_transcript(video_id, language_codes=['fr', 'en']):
    """Récupère la transcription YouTube"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        for lang in language_codes:
            try:
                transcript = transcript_list.find_transcript([lang])
                return transcript.fetch(), lang, transcript.is_generated
            except NoTranscriptFound:
                continue
        
        available_transcripts = list(transcript_list)
        if available_transcripts:
            transcript = available_transcripts[0]
            return transcript.fetch(), transcript.language_code, transcript.is_generated
        
        return None, None, None
        
    except TranscriptsDisabled:
        raise Exception("Les sous-titres sont désactivés pour cette vidéo")
    except NoTranscriptFound:
        raise Exception("Aucune transcription disponible pour cette vidéo")
    except VideoUnavailable:
        raise Exception("Vidéo non disponible")
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération de la transcription : {str(e)}")


def format_transcript_to_markdown(transcript, video_id, language):
    """Convertit la transcription en markdown avec timestamps cliquables"""
    
    markdown_lines = [
        f"# Transcription YouTube",
        f"",
        f"**Vidéo** : https://www.youtube.com/watch?v={video_id}",
        f"**Langue** : {language}",
        f"**Segments** : {len(transcript)}",
        f"",
        f"---",
        f""
    ]
    
    for entry in transcript:
        timestamp = format_timestamp(entry['start'])
        seconds = int(entry['start'])
        text = entry['text'].strip()
        
        link = f"[⏱️ {timestamp}](https://www.youtube.com/watch?v={video_id}&t={seconds}s)"
        
        markdown_lines.append(f"{link} {text}")
        markdown_lines.append("")
    
    return "\n".join(markdown_lines)


class handler(BaseHTTPRequestHandler):
    """Fonction principale Vercel"""
    
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers(200)
        self.wfile.write(b'')
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            body = json.loads(post_data.decode('utf-8'))
            youtube_url = body.get('url')
            languages = body.get('languages', ['fr', 'en'])
            
            if not youtube_url:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'URL YouTube manquante'}).encode())
                return
            
            video_id = extract_video_id(youtube_url)
            if not video_id:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'URL YouTube invalide'}).encode())
                return
            
            transcript, language, is_generated = get_transcript(video_id, languages)
            
            if not transcript:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Aucune transcription disponible'}).encode())
                return
            
            markdown = format_transcript_to_markdown(transcript, video_id, language)
            
            response = {
                'success': True,
                'video_id': video_id,
                'language': language,
                'is_generated': is_generated,
                'segments_count': len(transcript),
                'markdown': markdown
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode())
```

4. Clique **"Commit changes"**

---

## ✅ Étape 4 : Attends le redéploiement

1. Retourne sur **Vercel** : https://vercel.com/dashboard
2. Clique sur ton projet
3. Tu devrais voir un nouveau déploiement en cours
4. Attends 1-2 minutes ⏱️

---

## 🧪 Étape 5 : Teste l'API

Une fois le déploiement terminé :

1. Va sur **reqbin.com**
2. Change pour **POST**
3. URL : 
```
   https://ton-site.vercel.app/api/youtube_transcript
