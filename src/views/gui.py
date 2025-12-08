"""
MusicGeneratorGUI Class - Main application interface

This is the VIEW layer using Tkinter for GUI.

Author: [Nama Kamu]
Date: December 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from src.models.emotion import BasicEmotion


class MusicGeneratorGUI:
    """
    Main GUI application for Emotion-Based Music Generator.
    
    Uses Tkinter for cross-platform GUI.
    """
    
    def __init__(self, user, recommender, player, songs):
        """
        Initialize GUI.
        
        Args:
            user: User object
            recommender: RecommendationEngine object
            player: MusicPlayer object
            songs (list): List of Song objects
        """
        self.user = user
        self.recommender = recommender
        self.player = player
        self.songs = songs
        self.current_playlist = None
        
        # Create main window
        self.window = tk.Tk()
        self.window.title("🎵 Emotion-Based Music Generator")
        self.window.geometry("900x700")
        self.window.configure(bg='#1e1e2e')
        
        # Setup GUI components
        self._setup_ui()
        
        print("✓ GUI initialized")
    
    def _setup_ui(self):
        """Setup all UI components."""
        # Title
        title_frame = tk.Frame(self.window, bg='#1e1e2e')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🎵 Emotion-Based Music Generator",
            font=("Arial", 24, "bold"),
            bg='#1e1e2e',
            fg='#cdd6f4'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text=f"Welcome, {self.user.get_username()}!",
            font=("Arial", 12),
            bg='#1e1e2e',
            fg='#89b4fa'
        )
        subtitle_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.window, bg='#1e1e2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Emotion selection
        self._create_emotion_panel(content_frame)
        
        # Right panel - Playlist & Player
        self._create_playlist_panel(content_frame)
    
    def _create_emotion_panel(self, parent):
        """Create emotion selection panel."""
        left_frame = tk.Frame(parent, bg='#313244', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Header
        header = tk.Label(
            left_frame,
            text="Select Your Mood",
            font=("Arial", 16, "bold"),
            bg='#313244',
            fg='#cdd6f4'
        )
        header.pack(pady=15)
        
        # Emotions
        emotions = [
            ("😊 Happy", "happy", "#a6e3a1"),
            ("😢 Sad", "sad", "#94e2d5"),
            ("😌 Calm", "calm", "#89b4fa"),
            ("⚡ Energetic", "energetic", "#f9e2af"),
            ("😰 Stressed", "stressed", "#f38ba8"),
            ("😠 Angry", "angry", "#eba0ac"),
            ("😴 Tired", "tired", "#b4befe"),
            ("😐 Bored", "bored", "#cba6f7")
        ]
        
        for label, emotion, color in emotions:
            btn = tk.Button(
                left_frame,
                text=label,
                font=("Arial", 12),
                bg=color,
                fg='#1e1e2e',
                activebackground=color,
                cursor="hand2",
                relief=tk.FLAT,
                padx=20,
                pady=10,
                command=lambda e=emotion: self._on_emotion_selected(e)
            )
            btn.pack(fill=tk.X, padx=20, pady=5)
        
        # Intensity slider
        intensity_frame = tk.Frame(left_frame, bg='#313244')
        intensity_frame.pack(pady=15, padx=20, fill=tk.X)
        
        tk.Label(
            intensity_frame,
            text="Intensity:",
            font=("Arial", 11),
            bg='#313244',
            fg='#cdd6f4'
        ).pack(anchor=tk.W)
        
        self.intensity_var = tk.IntVar(value=5)
        self.intensity_slider = tk.Scale(
            intensity_frame,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.intensity_var,
            bg='#313244',
            fg='#cdd6f4',
            highlightthickness=0,
            troughcolor='#45475a',
            activebackground='#89b4fa'
        )
        self.intensity_slider.pack(fill=tk.X)
        
        self.intensity_label = tk.Label(
            intensity_frame,
            text="Level: 5/10",
            font=("Arial", 10),
            bg='#313244',
            fg='#89b4fa'
        )
        self.intensity_label.pack()
        
        self.intensity_var.trace('w', self._on_intensity_changed)
    
    def _create_playlist_panel(self, parent):
        """Create playlist and player panel."""
        right_frame = tk.Frame(parent, bg='#313244', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Playlist header
        playlist_header = tk.Label(
            right_frame,
            text="🎵 Recommended Playlist",
            font=("Arial", 16, "bold"),
            bg='#313244',
            fg='#cdd6f4'
        )
        playlist_header.pack(pady=15)
        
        # Playlist info
        self.playlist_info_label = tk.Label(
            right_frame,
            text="Select a mood to generate playlist",
            font=("Arial", 10),
            bg='#313244',
            fg='#89b4fa'
        )
        self.playlist_info_label.pack()
        
        # Song list
        list_frame = tk.Frame(right_frame, bg='#313244')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.song_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 10),
            bg='#45475a',
            fg='#cdd6f4',
            selectbackground='#89b4fa',
            selectforeground='#1e1e2e',
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.song_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.song_listbox.bind('<<ListboxSelect>>', self._on_song_selected)
        
        scrollbar.config(command=self.song_listbox.yview)
        
        # Now playing
        self.now_playing_label = tk.Label(
            right_frame,
            text="♪ Not playing",
            font=("Arial", 11, "italic"),
            bg='#313244',
            fg='#f9e2af'
        )
        self.now_playing_label.pack(pady=10)
        
        # Player controls
        self._create_player_controls(right_frame)
        
        # Stats button
        stats_btn = tk.Button(
            right_frame,
            text="📊 View Statistics",
            font=("Arial", 10),
            bg='#89b4fa',
            fg='#1e1e2e',
            activebackground='#74c7ec',
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            command=self._show_statistics
        )
        stats_btn.pack(pady=10)
    
    def _create_player_controls(self, parent):
        """Create player control buttons."""
        control_frame = tk.Frame(parent, bg='#313244')
        control_frame.pack(pady=15)
        
        btn_config = {
            'font': ("Arial", 10, "bold"),
            'relief': tk.FLAT,
            'cursor': "hand2",
            'padx': 15,
            'pady': 8
        }
        
        # Previous
        self.btn_prev = tk.Button(
            control_frame,
            text="⏮ Previous",
            bg='#45475a',
            fg='#cdd6f4',
            activebackground='#585b70',
            command=self._play_previous,
            **btn_config
        )
        self.btn_prev.grid(row=0, column=0, padx=5)
        
        # Play/Pause
        self.btn_play = tk.Button(
            control_frame,
            text="▶ Play",
            bg='#a6e3a1',
            fg='#1e1e2e',
            activebackground='#94e2d5',
            command=self._toggle_play_pause,
            **btn_config
        )
        self.btn_play.grid(row=0, column=1, padx=5)
        
        # Stop
        self.btn_stop = tk.Button(
            control_frame,
            text="⏹ Stop",
            bg='#f38ba8',
            fg='#1e1e2e',
            activebackground='#eba0ac',
            command=self._stop_playback,
            **btn_config
        )
        self.btn_stop.grid(row=0, column=2, padx=5)
        
        # Next
        self.btn_next = tk.Button(
            control_frame,
            text="Next ⏭",
            bg='#45475a',
            fg='#cdd6f4',
            activebackground='#585b70',
            command=self._play_next,
            **btn_config
        )
        self.btn_next.grid(row=0, column=3, padx=5)
        
        # Volume controls
        volume_frame = tk.Frame(parent, bg='#313244')
        volume_frame.pack()
        
        tk.Label(
            volume_frame,
            text="🔊 Volume:",
            font=("Arial", 10),
            bg='#313244',
            fg='#cdd6f4'
        ).pack(side=tk.LEFT, padx=5)
        
        self.volume_var = tk.IntVar(value=70)
        volume_scale = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.volume_var,
            command=self._on_volume_changed,
            bg='#313244',
            fg='#cdd6f4',
            highlightthickness=0,
            troughcolor='#45475a',
            activebackground='#89b4fa',
            length=200
        )
        volume_scale.pack(side=tk.LEFT)
    
    # ==================== EVENT HANDLERS ====================
    
    def _on_emotion_selected(self, emotion_type):
        """Handle emotion button click."""
        intensity = self.intensity_var.get()
        
        print(f"\n{'='*50}")
        print(f"User selected: {emotion_type} (intensity: {intensity})")
        
        # Create emotion object
        emotion_id = f"emo_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        emotion = BasicEmotion(emotion_id, emotion_type, intensity)
        
        # Record mood
        self.user.record_mood(emotion)
        
        # Generate playlist
        playlist = self.recommender.recommend_for_emotion(emotion, self.user, count=10)
        self.current_playlist = playlist
        
        # Update playlist display
        self._update_playlist_display(playlist)
        
        # Load playlist to player
        self.player.load_playlist(playlist)
        
        messagebox.showinfo(
            "Playlist Generated!",
            f"Generated {playlist.get_song_count()} songs for {emotion_type} mood!"
        )
    
    def _on_song_selected(self, event):
        """Handle song selection from listbox."""
        selection = self.song_listbox.curselection()
        if selection:
            index = selection[0]
            self.player.play_song_at_index(index)
            self._update_now_playing()
    
    def _on_intensity_changed(self, *args):
        """Handle intensity slider change."""
        value = self.intensity_var.get()
        self.intensity_label.config(text=f"Level: {value}/10")
    
    def _on_volume_changed(self, value):
        """Handle volume slider change."""
        volume = float(value) / 100.0
        self.player.set_volume(volume)
    
    def _toggle_play_pause(self):
        """Toggle play/pause."""
        if self.player.is_paused():
            self.player.resume()
            self.btn_play.config(text="⏸ Pause")
        elif self.player.is_playing():
            self.player.pause()
            self.btn_play.config(text="▶ Play")
        else:
            # Start playing first song
            if self.current_playlist and not self.current_playlist.is_empty():
                song = self.current_playlist.get_current_song()
                self.player.play(song)
                self.btn_play.config(text="⏸ Pause")
                self._update_now_playing()
    
    def _stop_playback(self):
        """Stop playback."""
        self.player.stop()
        self.btn_play.config(text="▶ Play")
        self.now_playing_label.config(text="♪ Stopped")
    
    def _play_previous(self):
        """Play previous song."""
        if self.player.previous():
            self._update_now_playing()
    
    def _play_next(self):
        """Play next song."""
        if self.player.next():
            self._update_now_playing()
    
    def _show_statistics(self):
        """Show statistics window."""
        stats_window = tk.Toplevel(self.window)
        stats_window.title("📊 Mood Statistics")
        stats_window.geometry("500x400")
        stats_window.configure(bg='#1e1e2e')
        
        # Get statistics
        stats = self.user.get_mood_statistics()
        
        # Display
        text_area = scrolledtext.ScrolledText(
            stats_window,
            font=("Courier", 10),
            bg='#313244',
            fg='#cdd6f4',
            wrap=tk.WORD
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        stats_text = f"""
{'='*50}
📊 YOUR MOOD STATISTICS
{'='*50}

Total Records: {stats['total_records']}

Most Common Mood: {stats.get('most_common_mood', 'N/A')}
   Count: {stats.get('most_common_count', 0)} times

Average Intensity: {stats['average_intensity']}/10

Favorite Listening Time: {stats.get('favorite_time', 'N/A')}

{'='*50}
MOOD DISTRIBUTION:
{'='*50}
"""
        
        for mood, count in stats['mood_distribution'].items():
            stats_text += f"\n{mood.capitalize():15} : {count} times"
        
        text_area.insert('1.0', stats_text)
        text_area.config(state=tk.DISABLED)
    
    # ==================== UI UPDATE METHODS ====================
    
    def _update_playlist_display(self, playlist):
        """Update playlist display."""
        self.song_listbox.delete(0, tk.END)
        
        for i, song in enumerate(playlist.get_songs(), 1):
            display_text = f"{i}. {song.get_title()} - {song.get_artist()}"
            self.song_listbox.insert(tk.END, display_text)
        
        self.playlist_info_label.config(
            text=f"Playlist: {playlist.get_name()} | {playlist.get_song_count()} songs"
        )
    
    def _update_now_playing(self):
        """Update now playing label."""
        song = self.player.get_current_song()
        if song:
            text = f"♪ Now Playing: {song.get_title()} - {song.get_artist()}"
            self.now_playing_label.config(text=text)
    
    # ==================== MAIN LOOP ====================
    
    def run(self):
        """Start the GUI main loop."""
        self.window.mainloop()
    
    def __del__(self):
        """Cleanup when GUI closes."""
        try:
            self.player.cleanup()
        except:
            pass


# ==================== TESTING ====================
if __name__ == "__main__":
    print("GUI module loaded")
    print("Run main.py to start the application")