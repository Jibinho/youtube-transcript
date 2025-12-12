#!/usr/bin/env python3
"""Script de test local pour le service de transcription YouTube"""

import json
import sys

sys.path.insert(0, 'functions')
from youtube_transcript import extract_video_id, get_transcript, format_transcript_to_markdown


def test_transcript(url):
    """Teste le workflow complet"""
    print(f"🔍 Test de l'URL : {url}\n")
    
    # 1. Extraction de l'ID
    video_id = extract_video_id(url)
    if not video_id:
        print("❌ Impossible d'extraire l'ID vidéo")
        return
    
    print(f"✅ ID vidéo : {video_id}")
    
    # 2. Récupération de la transcription
    try:
        transcript, language, is_generated = get_transcript(video_id)
        print(f"✅ Transcription trouvée")
        print(f"   Langue : {language}")
        print(f"   Type : {'Générée automatiquement' if is_generated else 'Officielle'}")
        print(f"   Segments : {len(transcript)}")
        
        # Aperçu du premier segment
        if transcript:
            print(f"\n📝 Premier segment :")
            print(f"   Timestamp : {transcript[0]['start']:.2f}s")
            print(f"   Texte : {transcript[0]['text'][:100]}...")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return
    
    # 3. Formatage en markdown
    print(f"\n📄 Génération du markdown...")
    markdown = format_transcript_to_markdown(transcript, video_id, language)
    print(f"✅ Markdown généré ({len(markdown)} caractères)")
    
    # Aperçu
    print(f"\n--- APERÇU ---")
    print(markdown[:500] + "...\n")
    
    # Sauvegarde
    output_file = f"transcript_{video_id}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    print(f"💾 Sauvegardé dans : {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_transcript.py <URL_YOUTUBE>")
        print("\nExemples d'URLs supportées :")
        print("  - https://www.youtube.com/watch?v=VIDEO_ID")
        print("  - https://youtu.be/VIDEO_ID")
        print("  - https://www.youtube.com/shorts/VIDEO_ID")
        sys.exit(1)
    
    test_transcript(sys.argv[1])
