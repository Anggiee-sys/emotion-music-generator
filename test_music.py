import pygame
import os

print("Testing MP3 playback...")

# Get absolute path
base_dir = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(base_dir, 'assets', 'music', 'calmsong1.mp3')

print(f"Testing file: {mp3_path}")
print(f"File exists: {os.path.exists(mp3_path)}")

if os.path.exists(mp3_path):
    try:
        # Initialize pygame
        pygame.mixer.init()
        print("✓ Pygame initialized")
        
        # Load and play
        pygame.mixer.music.load(mp3_path)
        print("✓ File loaded")
        
        pygame.mixer.music.play()
        print("✓ Playing... (press Ctrl+C to stop)")
        
        # Wait
        import time
        time.sleep(5)
        
        pygame.mixer.music.stop()
        print("✓ Stopped")
        
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("✗ File not found!")