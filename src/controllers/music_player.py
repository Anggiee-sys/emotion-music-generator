"""
MusicPlayer Class - Controls music playback

This class demonstrates ENCAPSULATION through:
- Private playback state management
- Controlled audio operations

Requires: pygame library
Install with: pip install pygame

Author: [Nama Kamu]
Date: December 2025
"""

import pygame
import os


class MusicPlayer:
    """
    Handles music playback using pygame.mixer.
    
    Attributes:
        __current_song: Currently loaded Song object
        __current_playlist: Currently loaded Playlist object
        __is_playing (bool): Whether music is currently playing
        __is_paused (bool): Whether music is paused
        __volume (float): Volume level (0.0 - 1.0)
        __current_position (float): Current playback position in seconds
    """
    
    def __init__(self):
        """
        Initialize MusicPlayer and pygame mixer.
        """
        # ENCAPSULATION: Private attributes
        self.__current_song = None
        self.__current_playlist = None
        self.__is_playing = False
        self.__is_paused = False
        self.__volume = 0.7  # Default volume 70%
        self.__current_position = 0.0
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.__volume)
            print("✓ Music player initialized")
        except Exception as e:
            print(f"✗ Error initializing music player: {e}")
            raise
    
    # ==================== GETTER METHODS ====================
    
    def get_current_song(self):
        """Get currently loaded song."""
        return self.__current_song
    
    def get_current_playlist(self):
        """Get currently loaded playlist."""
        return self.__current_playlist
    
    def is_playing(self):
        """Check if music is playing."""
        return self.__is_playing and pygame.mixer.music.get_busy()
    
    def is_paused(self):
        """Check if music is paused."""
        return self.__is_paused
    
    def get_volume(self):
        """Get current volume level."""
        return self.__volume
    
    def get_current_position(self):
        """
        Get current playback position.
        
        Returns:
            float: Position in seconds
        """
        if self.__is_playing:
            return pygame.mixer.music.get_pos() / 1000.0  # Convert ms to seconds
        return self.__current_position
    
    def get_playback_status(self):
        """
        Get complete playback status.
        
        Returns:
            dict: Status information
        """
        status = {
            'is_playing': self.is_playing(),
            'is_paused': self.__is_paused,
            'volume': self.__volume,
            'current_song': None,
            'current_playlist': None
        }
        
        if self.__current_song:
            status['current_song'] = {
                'title': self.__current_song.get_title(),
                'artist': self.__current_song.get_artist(),
                'duration': self.__current_song.get_duration()
            }
        
        if self.__current_playlist:
            status['current_playlist'] = {
                'name': self.__current_playlist.get_name(),
                'total_songs': self.__current_playlist.get_song_count(),
                'current_index': self.__current_playlist.get_current_index()
            }
        
        return status
    
    # ==================== PLAYBACK CONTROL ====================
    
    def play(self, song):
        """
        Play a song.
        
        Args:
            song: Song object to play
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(song.get_file_path()):
                print(f"✗ File not found: {song.get_file_path()}")
                return False
            
            # Load and play
            pygame.mixer.music.load(song.get_file_path())
            pygame.mixer.music.play()
            
            # Update state
            self.__current_song = song
            self.__is_playing = True
            self.__is_paused = False
            self.__current_position = 0.0
            
            # Increment play count
            song.increment_play_count()
            
            print(f"▶ Now playing: {song.get_title()} - {song.get_artist()}")
            return True
            
        except Exception as e:
            print(f"✗ Error playing song: {e}")
            self.__is_playing = False
            return False
    
    def pause(self):
        """
        Pause current playback.
        
        Returns:
            bool: True if paused, False if nothing playing
        """
        if self.__is_playing and not self.__is_paused:
            pygame.mixer.music.pause()
            self.__is_paused = True
            self.__current_position = self.get_current_position()
            print("⏸ Paused")
            return True
        return False
    
    def resume(self):
        """
        Resume paused playback.
        
        Returns:
            bool: True if resumed, False if not paused
        """
        if self.__is_paused:
            pygame.mixer.music.unpause()
            self.__is_paused = False
            print("▶ Resumed")
            return True
        return False
    
    def stop(self):
        """
        Stop current playback.
        
        Returns:
            bool: True if stopped
        """
        if self.__is_playing or self.__is_paused:
            pygame.mixer.music.stop()
            self.__is_playing = False
            self.__is_paused = False
            self.__current_position = 0.0
            print("⏹ Stopped")
            return True
        return False
    
    def toggle_play_pause(self):
        """
        Toggle between play and pause.
        
        Returns:
            bool: Current playing state
        """
        if self.__is_paused:
            self.resume()
        elif self.__is_playing:
            self.pause()
        return self.__is_playing
    
    # ==================== PLAYLIST CONTROL ====================
    
    def load_playlist(self, playlist):
        """
        Load a playlist for playback.
        
        Args:
            playlist: Playlist object
            
        Returns:
            bool: True if loaded successfully
        """
        if playlist and not playlist.is_empty():
            self.__current_playlist = playlist
            playlist.reset_position()
            print(f"✓ Loaded playlist: {playlist.get_name()} ({playlist.get_song_count()} songs)")
            return True
        else:
            print("✗ Cannot load empty playlist")
            return False
    
    def play_playlist(self, playlist):
        """
        Load and play first song of playlist.
        
        Args:
            playlist: Playlist object
            
        Returns:
            bool: True if started playing
        """
        if self.load_playlist(playlist):
            first_song = playlist.get_current_song()
            if first_song:
                return self.play(first_song)
        return False
    
    def next(self):
        """
        Play next song in playlist.
        
        Returns:
            bool: True if there's a next song, False otherwise
        """
        if self.__current_playlist:
            next_song = self.__current_playlist.next_song()
            if next_song:
                return self.play(next_song)
            else:
                print("⏭ No next song (end of playlist)")
                return False
        else:
            print("✗ No playlist loaded")
            return False
    
    def previous(self):
        """
        Play previous song in playlist.
        
        Returns:
            bool: True if there's a previous song
        """
        if self.__current_playlist:
            prev_song = self.__current_playlist.previous_song()
            if prev_song:
                return self.play(prev_song)
            else:
                print("⏮ No previous song (start of playlist)")
                return False
        else:
            print("✗ No playlist loaded")
            return False
    
    def play_song_at_index(self, index):
        """
        Play specific song from playlist by index.
        
        Args:
            index (int): Song index in playlist
            
        Returns:
            bool: True if successful
        """
        if self.__current_playlist:
            try:
                self.__current_playlist.set_current_index(index)
                song = self.__current_playlist.get_current_song()
                if song:
                    return self.play(song)
            except ValueError as e:
                print(f"✗ Invalid index: {e}")
        return False
    
    # ==================== VOLUME CONTROL ====================
    
    def set_volume(self, volume):
        """
        Set playback volume.
        
        Args:
            volume (float): Volume level (0.0 - 1.0)
        """
        # Validate and clamp volume
        volume = max(0.0, min(1.0, float(volume)))
        self.__volume = volume
        pygame.mixer.music.set_volume(volume)
    
    def increase_volume(self, amount=0.1):
        """
        Increase volume by amount.
        
        Args:
            amount (float): Amount to increase (default 0.1)
        """
        new_volume = min(1.0, self.__volume + amount)
        self.set_volume(new_volume)
        print(f"🔊 Volume: {int(new_volume * 100)}%")
    
    def decrease_volume(self, amount=0.1):
        """
        Decrease volume by amount.
        
        Args:
            amount (float): Amount to decrease (default 0.1)
        """
        new_volume = max(0.0, self.__volume - amount)
        self.set_volume(new_volume)
        print(f"🔉 Volume: {int(new_volume * 100)}%")
    
    def mute(self):
        """Mute audio (set volume to 0)."""
        self.set_volume(0.0)
        print("🔇 Muted")
    
    def unmute(self):
        """Unmute audio (restore to 70%)."""
        self.set_volume(0.7)
        print(f"🔊 Volume: 70%")
    
    # ==================== UTILITY METHODS ====================
    
    def is_song_finished(self):
        """
        Check if current song finished playing.
        
        Returns:
            bool: True if finished
        """
        return self.__is_playing and not pygame.mixer.music.get_busy()
    
    def cleanup(self):
        """
        Cleanup and stop all playback.
        Safe to call when closing application.
        """
        try:
            self.stop()
            pygame.mixer.quit()
            print("✓ Music player cleaned up")
        except:
            pass
    
    # ==================== STRING REPRESENTATION ====================
    
    def __str__(self):
        """String representation."""
        status = "Playing" if self.__is_playing else "Paused" if self.__is_paused else "Stopped"
        song_info = ""
        if self.__current_song:
            song_info = f" - {self.__current_song.get_title()}"
        return f"MusicPlayer [{status}]{song_info}"
    
    def __repr__(self):
        """Debug representation."""
        return f"MusicPlayer(playing={self.__is_playing}, paused={self.__is_paused}, volume={self.__volume})"


# ==================== TESTING ====================
if __name__ == "__main__":
    print("Testing MusicPlayer Class...")
    print("=" * 60)
    
    # Note: This test requires actual MP3 files to work
    print("\n⚠ Note: Full testing requires MP3 files")
    print("Creating player instance...")
    
    try:
        player = MusicPlayer()
        print(f"✓ Player created: {player}")
        print(f"Volume: {int(player.get_volume() * 100)}%")
        print(f"Is playing: {player.is_playing()}")
        
        # Test volume controls
        print("\n--- Testing Volume Control ---")
        player.increase_volume(0.2)
        print(f"Volume after increase: {int(player.get_volume() * 100)}%")
        
        player.decrease_volume(0.1)
        print(f"Volume after decrease: {int(player.get_volume() * 100)}%")
        
        # Get status
        print("\n--- Playback Status ---")
        status = player.get_playback_status()
        print(f"Status: {status}")
        
        print("\n" + "=" * 60)
        print("✓ Basic tests completed!")
        print("To test playback, run main.py with actual songs")
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")