print("Testing imports...")

try:
    from src.models.song import Song
    print("✓ Song imported")
except Exception as e:
    print(f"✗ Song failed: {e}")

try:
    from src.models.emotion import Emotion, BasicEmotion
    print("✓ Emotion imported")
except Exception as e:
    print(f"✗ Emotion failed: {e}")

try:
    from src.models.user import User
    print("✓ User imported")
except Exception as e:
    print(f"✗ User failed: {e}")

try:
    from src.models.playlist import Playlist
    print("✓ Playlist imported")
except Exception as e:
    print(f"✗ Playlist failed: {e}")

try:
    from src.controllers.music_player import MusicPlayer
    print("✓ MusicPlayer imported")
except Exception as e:
    print(f"✗ MusicPlayer failed: {e}")

try:
    from src.controllers.recommendation_engine import RuleBasedRecommender
    print("✓ RecommendationEngine imported")
except Exception as e:
    print(f"✗ RecommendationEngine failed: {e}")

try:
    from src.views.gui import MusicGeneratorGUI
    print("✓ GUI imported")
except Exception as e:
    print(f"✗ GUI failed: {e}")

print("\nAll imports successful!")