import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)


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
        
        # Cherche une transcription dans les langues préférées
        for lang in language_codes:
            try:
                transcript = transcript_list.find_transcript([lang])
                return transcript.fetch(), lang, transcript.is_generated
            except NoTranscriptFound:
                continue
        
        # Si aucune langue préférée, prend la première disponible
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
        
        # Crée un lien cliquable vers le timestamp
        link = f"[⏱️ {timestamp}](https://www.youtube.com/watch?v={video_id}&t={seconds}s)"
        
        markdown_lines.append(f"{link} {text}")
        markdown_lines.append("")
    
    return "\n".join(markdown_lines)


def handler(event, context):
    """Fonction principale Netlify"""
    
    # Gestion CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }
    
    # Gestion preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Méthode non autorisée. Utilisez POST.'})
        }
    
    try:
        # Parse le body
        body = json.loads(event['body'])
        youtube_url = body.get('url')
        languages = body.get('languages', ['fr', 'en'])
        
        if not youtube_url:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'URL YouTube manquante'})
            }
        
        # Extrait l'ID vidéo
        video_id = extract_video_id(youtube_url)
        if not video_id:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'URL YouTube invalide'})
            }
        
        # Récupère la transcription
        transcript, language, is_generated = get_transcript(video_id, languages)
        
        if not transcript:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Aucune transcription disponible'})
            }
        
        # Formate en markdown
        markdown = format_transcript_to_markdown(transcript, video_id, language)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'success': True,
                'video_id': video_id,
                'language': language,
                'is_generated': is_generated,
                'segments_count': len(transcript),
                'markdown': markdown
            }, ensure_ascii=False)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }
