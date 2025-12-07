"""
Emotion-Based Music Generator
Main Entry Point

Project: OOP Final Project
Author: [Anggietha Isyah Prameswari] - [24091397079]
Date: December 2025
Description: Aplikasi untuk menghasilkan playlist musik berdasarkan mood/emosi pengguna
"""

import json
import os
import sys
from src.models.user import User
from src.models.song import Song
from src.controllers.recommendation_engine import RuleBasedRecommender
from src.controllers.music_player import MusicPlayer
from src.views.gui import MusicGeneratorGUI


def load_songs_from_json():
    """
    Load song database from JSON file.
    If file doesn't exist, create default songs from assets/music folder.
    
    Returns:
        list: List of Song objects
    """
    json_path = "data/songs.json"
    
    # Check if JSON file exists
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                songs_data = json.load(file)
                songs = []
                
                print(f"Loading songs from {json_path}...")
                for song_data in songs_data:
                    # Validate file exists
                    if os.path.exists(song_data['file_path']):
                        song = Song(
                            song_id=song_data['song_id'],
                            title=song_data['title'],
                            artist=song_data['artist'],
                            file_path=song_data['file_path'],
                            mood_tags=song_data['mood_tags'],
                            tempo=song_data['tempo'],
                            genre=song_data.get('genre', 'Unknown'),
                            duration=song_data.get('duration', 0)
                        )
                        songs.append(song)
                    else:
                        print(f"  ⚠ Warning: File not found - {song_data['file_path']}")
                
                print(f"✓ Loaded {len(songs)} songs from {json_path}")
                return songs
                
        except json.JSONDecodeError as e:
            print(f"✗ Error parsing JSON: {e}")
            print("Creating default songs...")
            return create_default_songs()
        except Exception as e:
            print(f"✗ Error loading songs from JSON: {e}")
            print("Creating default songs...")
            return create_default_songs()
    else:
        print(f"✗ {json_path} not found. Creating default songs...")
        return create_default_songs()


def create_default_songs():
    """
    Create default song objects from assets/music folder.
    Based on actual MP3 files: 12 songs (3 calm, 3 energetic, 3 happy, 3 sad)
    
    Returns:
        list: List of default Song objects
    """
    songs = []
    
    # Define default songs based on your actual MP3 files
    default_songs = [
        # ========== CALM SONGS (3) ==========
        {
            'song_id': 'song_001',
            'title': 'Calm Song 1',
            'artist': 'Relaxing Music',
            'file_path': 'assets/music/calmsong1.mp3',
            'mood_tags': ['calm', 'relaxed', 'peaceful', 'meditation'],
            'tempo': 'slow',
            'genre': 'Ambient',
            'duration': 180
        },
        {
            'song_id': 'song_002',
            'title': 'Calm Song 2',
            'artist': 'Relaxing Music',
            'file_path': 'assets/music/calmsong2.mp3',
            'mood_tags': ['calm', 'relaxed', 'peaceful', 'sleep'],
            'tempo': 'slow',
            'genre': 'Ambient',
            'duration': 185
        },
        {
            'song_id': 'song_003',
            'title': 'Calm Song 3',
            'artist': 'Relaxing Music',
            'file_path': 'assets/music/calmsong3.mp3',
            'mood_tags': ['calm', 'relaxed', 'peaceful', 'focus'],
            'tempo': 'slow',
            'genre': 'Ambient',
            'duration': 190
        },
        
        # ========== ENERGETIC SONGS (3) ==========
        {
            'song_id': 'song_004',
            'title': 'Energetic Song 1',
            'artist': 'Workout Beats',
            'file_path': 'assets/music/energeticsong1.mp3',
            'mood_tags': ['energetic', 'motivated', 'active', 'workout'],
            'tempo': 'fast',
            'genre': 'Electronic',
            'duration': 200
        },
        {
            'song_id': 'song_005',
            'title': 'Energetic Song 2',
            'artist': 'Workout Beats',
            'file_path': 'assets/music/energeticsong2.mp3',
            'mood_tags': ['energetic', 'motivated', 'active', 'exercise'],
            'tempo': 'fast',
            'genre': 'Electronic',
            'duration': 195
        },
        {
            'song_id': 'song_006',
            'title': 'Energetic Song 3',
            'artist': 'Workout Beats',
            'file_path': 'assets/music/energeticsong3.mp3',
            'mood_tags': ['energetic', 'motivated', 'active', 'pump'],
            'tempo': 'fast',
            'genre': 'Electronic',
            'duration': 205
        },
        
        # ========== HAPPY SONGS (3) ==========
        {
            'song_id': 'song_007',
            'title': 'Happy Song 1',
            'artist': 'Cheerful Vibes',
            'file_path': 'assets/music/happysong1.mp3',
            'mood_tags': ['happy', 'joyful', 'cheerful', 'upbeat'],
            'tempo': 'medium',
            'genre': 'Pop',
            'duration': 190
        },
        {
            'song_id': 'song_008',
            'title': 'Happy Song 2',
            'artist': 'Cheerful Vibes',
            'file_path': 'assets/music/happysong2.mp3',
            'mood_tags': ['happy', 'joyful', 'cheerful', 'fun'],
            'tempo': 'medium',
            'genre': 'Pop',
            'duration': 185
        },
        {
            'song_id': 'song_009',
            'title': 'Happy Song 3',
            'artist': 'Cheerful Vibes',
            'file_path': 'assets/music/happysong3.mp3',
            'mood_tags': ['happy', 'joyful', 'cheerful', 'positive'],
            'tempo': 'medium',
            'genre': 'Pop',
            'duration': 195
        },
        
        # ========== SAD SONGS (3) ==========
        {
            'song_id': 'song_010',
            'title': 'Sad Song 1',
            'artist': 'Melancholic Soul',
            'file_path': 'assets/music/sadsong1.mp3',
            'mood_tags': ['sad', 'melancholic', 'emotional', 'heartbreak'],
            'tempo': 'slow',
            'genre': 'Ballad',
            'duration': 210
        },
        {
            'song_id': 'song_011',
            'title': 'Sad Song 2',
            'artist': 'Melancholic Soul',
            'file_path': 'assets/music/sadsong2.mp3',
            'mood_tags': ['sad', 'melancholic', 'emotional', 'lonely'],
            'tempo': 'slow',
            'genre': 'Ballad',
            'duration': 215
        },
        {
            'song_id': 'song_012',
            'title': 'Sad Song 3',
            'artist': 'Melancholic Soul',
            'file_path': 'assets/music/sadsong3.mp3',
            'mood_tags': ['sad', 'melancholic', 'emotional', 'grief'],
            'tempo': 'slow',
            'genre': 'Ballad',
            'duration': 220
        }
    ]
    
    # Create Song objects
    songs_created = 0
    songs_failed = 0
    
    print("\nCreating song database from MP3 files...")
    for song_data in default_songs:
        # Check if file exists
        if os.path.exists(song_data['file_path']):
            song = Song(
                song_id=song_data['song_id'],
                title=song_data['title'],
                artist=song_data['artist'],
                file_path=song_data['file_path'],
                mood_tags=song_data['mood_tags'],
                tempo=song_data['tempo'],
                genre=song_data['genre'],
                duration=song_data['duration']
            )
            songs.append(song)
            songs_created += 1
            print(f"  ✓ {song.get_title()} ({song.get_genre()})")
        else:
            songs_failed += 1
            print(f"  ✗ File not found: {song_data['file_path']}")
    
    print(f"\nSummary: {songs_created} songs loaded successfully")
    if songs_failed > 0:
        print(f"Warning: {songs_failed} songs failed to load")
    
    # Save to JSON for future use
    if songs:
        save_songs_to_json(songs)
    else:
        print("\n✗ ERROR: No songs were loaded!")
        print("Please ensure MP3 files exist in assets/music/ folder")
    
    return songs


def save_songs_to_json(songs):
    """
    Save song list to JSON file for faster loading next time.
    
    Args:
        songs (list): List of Song objects
    """
    json_path = "data/songs.json"
    
    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)
    
    # Convert Song objects to dictionaries
    songs_data = []
    for song in songs:
        song_dict = {
            'song_id': song.get_song_id(),
            'title': song.get_title(),
            'artist': song.get_artist(),
            'file_path': song.get_file_path(),
            'mood_tags': song.get_mood_tags(),
            'tempo': song.get_tempo(),
            'genre': song.get_genre(),
            'duration': song.get_duration()
        }
        songs_data.append(song_dict)
    
    # Save to JSON
    try:
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(songs_data, file, indent=4, ensure_ascii=False)
        print(f"✓ Songs database saved to {json_path}")
    except Exception as e:
        print(f"✗ Error saving songs to JSON: {e}")


def print_banner():
    """
    Print application banner/header.
    """
    print("\n" + "=" * 60)
    print("🎵  EMOTION-BASED MUSIC GENERATOR  🎵")
    print("=" * 60)
    print("Generate personalized playlists based on your mood")
    print("Developed by: [Nama Kamu] - [NIM]")
    print("=" * 60 + "\n")


def check_dependencies():
    """
    Check if all required dependencies are installed.
    
    Returns:
        bool: True if all dependencies available, False otherwise
    """
    missing_deps = []
    
    # Check pygame
    try:
        import pygame
    except ImportError:
        missing_deps.append('pygame')
    
    # Check matplotlib
    try:
        import matplotlib
    except ImportError:
        missing_deps.append('matplotlib')
    
    # Check pandas
    try:
        import pandas
    except ImportError:
        missing_deps.append('pandas')
    
    if missing_deps:
        print("✗ ERROR: Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install with: pip install " + " ".join(missing_deps))
        return False
    
    return True


def main():
    """
    Main function to initialize and run the application.
    This is the entry point of the program.
    """
    # Print banner
    print_banner()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("\n✗ Application cannot start due to missing dependencies.")
        input("Press Enter to exit...")
        sys.exit(1)
    print("✓ All dependencies installed\n")
    
    # Initialize user
    print("1. Initializing user profile...")
    user = User(user_id="user_001", username="Default User")
    print(f"   ✓ User created: {user.get_username()}\n")
    
    # Initialize recommendation engine
    print("2. Initializing recommendation engine...")
    recommender = RuleBasedRecommender()
    print("   ✓ Rule-based recommender ready\n")
    
    # Initialize music player
    print("3. Initializing music player...")
    try:
        player = MusicPlayer()
        print("   ✓ Music player initialized\n")
    except Exception as e:
        print(f"   ✗ Error initializing music player: {e}")
        print("   Please check if pygame is properly installed.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Load song database
    print("4. Loading song database...")
    songs = load_songs_from_json()
    
    if not songs:
        print("\n✗ ERROR: No songs found!")
        print("Please ensure MP3 files exist in assets/music/ folder:")
        print("  - calmsong1.mp3, calmsong2.mp3, calmsong3.mp3")
        print("  - energeticsong1.mp3, energeticsong2.mp3, energeticsong3.mp3")
        print("  - happysong1.mp3, happysong2.mp3, happysong3.mp3")
        print("  - sadsong1.mp3, sadsong2.mp3, sadsong3.mp3")
        print("\nApplication cannot start without songs.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"\n   ✓ Successfully loaded {len(songs)} songs")
    
    # Update recommender with song database
    print("\n5. Configuring recommendation system...")
    recommender.update_database(songs)
    print("   ✓ Recommendation engine configured\n")
    
    # Start GUI
    print("6. Starting GUI application...")
    print("=" * 60)
    print()
    
    try:
        app = MusicGeneratorGUI(user, recommender, player, songs)
        app.run()
    except KeyboardInterrupt:
        print("\n\n✓ Application closed by user")
    except Exception as e:
        print(f"\n✗ ERROR: Application crashed!")
        print(f"Error details: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
    finally:
        # Cleanup
        try:
            player.cleanup()
        except:
            pass
        print("\n✓ Application closed successfully")


if __name__ == "__main__":
    """
    Entry point - runs when script is executed directly.
    """
    try:
        main()
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)