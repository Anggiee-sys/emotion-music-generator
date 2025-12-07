# views/gui.py
import tkinter as tk
from tkinter import ttk

class MusicGeneratorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Emotion-Based Music Generator")
        
        # Components
        self.create_emotion_selector()
        self.create_playlist_viewer()
        self.create_player_controls()
        self.create_mood_stats()
    
    def create_emotion_selector(self):
        # Dropdown atau buttons untuk pilih emosi
        emotions = ['Happy', 'Sad', 'Calm', 'Energetic', 'Stressed']
        # ... buat UI
    
    def on_emotion_selected(self, emotion):
        # Trigger recommendation
        pass