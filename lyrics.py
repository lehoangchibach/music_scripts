import os
import json
import requests
from pathlib import Path
from mutagen import File as MutagenFile
from rapidfuzz import fuzz

# Configuration
INPUT_FOLDER = Path("../files/tmp")
OUTPUT_FOLDER = Path("../files/tmp")
API_URL = "https://lrclib.net/api/get"
SIMILARITY_THRESHOLD = 80.0  # Percentage threshold for validation

def extract_metadata(file_path):
    """Extracts track name, artist, album, and duration from an audio file."""
    try:
        audio = MutagenFile(file_path)
        if audio is None or audio.info is None:
            return None

        # Handle different tagging formats gracefully
        title = audio.get("title", [None])[0] or audio.get("TIT2", [None])[0]
        artist = audio.get("artist", [None])[0] or audio.get("TPE1", [None])[0]
        album = audio.get("album", [None])[0] or audio.get("TALB", [None])[0]
        duration = int(audio.info.length) if hasattr(audio.info, "length") else 0

        if not (title and artist and album and duration):
            return None

        return {
            "track_name": str(title),
            "artist_name": str(artist),
            "album_name": str(album),
            "duration": duration
        }
    except Exception as e:
        print(f"[-] Error parsing metadata for {file_path.name}: {e}")
        return None

def validate_metadata(local, remote):
    """Validates remote metadata against local metadata using fuzzy matching."""
    # Check artist and track name using token ratio (handles order/minor variations)
    artist_score = fuzz.token_sort_ratio(local["artist_name"].lower(), remote.get("artistName", "").lower())
    track_score = fuzz.token_sort_ratio(local["track_name"].lower(), remote.get("trackName", "").lower())
    
    return artist_score >= SIMILARITY_THRESHOLD and track_score >= SIMILARITY_THRESHOLD

def clean_log_response(data):
    """Removes bulky lyric fields from the JSON for clean logging."""
    clean_data = data.copy()
    clean_data.pop("syncedLyrics", None)
    clean_data.pop("plainLyrics", None)
    return json.dumps(clean_data, indent=2)

def process_files():
    # Ensure output directory exists
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    
    supported_extensions = {".mp3", ".flac", ".m4a"}
    
    # Filter files in the input directory
    files_to_process = [f for f in INPUT_FOLDER.iterdir() if f.suffix.lower() in supported_extensions]
    
    if not files_to_process:
        print("[!] No matching audio files found in the input folder.")
        return

    for file_path in files_to_process:
        print(f"\n{'='*60}\nProcessing: {file_path.name}")
        
        metadata = extract_metadata(file_path)
        if not metadata:
            print("[-] Missing metadata or unsupported tags. Skipping.")
            continue
        
        # Log Request Details
        print(f"Request parameters:\n{json.dumps(metadata, indent=2)}")
        
        try:
            response = requests.get(API_URL, params=metadata)
            
            if response.status_code == 404:
                print("[-] Response: 404 - Track Not Found")
                continue
            elif response.status_code != 200:
                print(f"[-] Response Error: {response.status_code}")
                continue
                
            res_data = response.json()
            print(f"Response (Lyrics Hidden):\n{clean_log_response(res_data)}")
            
            # Validate results using rapidfuzz
            if not validate_metadata(metadata, res_data):
                print("[-] Validation Failed: Metadata mismatch between file and API response.")
                continue
                
            # Determine content priority: syncedLyrics -> plainLyrics -> None
            lyrics_content = res_data.get("syncedLyrics") or res_data.get("plainLyrics")
            
            if not lyrics_content:
                print("[-] No lyrics content found in response.")
                continue
                
            # Write out the .lrc file
            output_file_path = OUTPUT_FOLDER / f"{file_path.stem}.lrc"
            output_file_path.write_text(lyrics_content, encoding="utf-8")
            print(f"[+] Successfully saved lyrics to: {output_file_path.name}")
            
        except Exception as e:
            print(f"[-] Error processing request for {file_path.name}: {e}")

if __name__ == "__main__":
    process_files()