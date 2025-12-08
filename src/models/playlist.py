"""
Playlist Class - Collection of songs

This class demonstrates ENCAPSULATION through:
- Private song collection management
- Controlled access and manipulation methods

Author: [Nama Kamu]
Date: December 2025
"""

from datetime import datetime
import random


class Playlist:
    """
    Represents a playlist of songs.
    
    Attributes:
        __playlist_id (str): Unique playlist identifier
        __name (str): Playlist name
        __songs (list): List of Song objects
        __created_for_emotion: Emotion object this playlist was created for
        __created_at (datetime): Creation timestamp
        __current_index (int): Current song index for playback
    """
    
    def __init__(self, playlist_id, name, created_for_emotion=None):
        """
        Initialize Playlist object.
        
        Args:
            playlist_id (str): Unique identifier
            name (str): Playlist name
            created_for_emotion: Emotion object (optional)
        """
        # ENCAPSULATION: Private attributes
        self.__playlist_id = playlist_id
        self.__name = name
        self.__songs = []
        self.__created_for_emotion = created_for_emotion
        self.__created_at = datetime.now()
        self.__current_index = 0
    
    # ==================== GETTER METHODS ====================
    
    def get_playlist_id(self):
        """Get playlist ID."""
        return self.__playlist_id
    
    def get_name(self):
        """Get playlist name."""
        return self.__name
    
    def get_songs(self):
        """
        Get list of songs (returns copy to prevent external modification).
        
        Returns:
            list: Songs in playlist
        """
        return self.__songs.copy()
    
    def get_song_count(self):
        """Get number of songs in playlist."""
        return len(self.__songs)
    
    def get_created_for_emotion(self):
        """Get emotion this playlist was created for."""
        return self.__created_for_emotion
    
    def get_created_at(self):
        """Get creation timestamp."""
        return self.__created_at
    
    def get_current_index(self):
        """Get current song index."""
        return self.__current_index
    
    def get_current_song(self):
        """
        Get currently selected song.
        
        Returns:
            Song: Current song or None if empty
        """
        if 0 <= self.__current_index < len(self.__songs):
            return self.__songs[self.__current_index]
        return None
    
    # ==================== SETTER METHODS ====================
    
    def set_name(self, name):
        """
        Set playlist name.
        
        Args:
            name (str): New playlist name
        """
        if name and len(name.strip()) > 0:
            self.__name = name.strip()
        else:
            raise ValueError("Playlist name cannot be empty")
    
    def set_current_index(self, index):
        """
        Set current song index with validation.
        
        Args:
            index (int): Song index
        """
        if 0 <= index < len(self.__songs):
            self.__current_index = index
        else:
            raise ValueError(f"Index out of range (0-{len(self.__songs)-1})")
    
    # ==================== SONG MANAGEMENT ====================
    
    def add_song(self, song):
        """
        Add a song to the playlist.
        
        Args:
            song: Song object to add
        """
        if song not in self.__songs:
            self.__songs.append(song)
            return True
        return False
    
    def add_songs(self, songs):
        """
        Add multiple songs to playlist.
        
        Args:
            songs (list): List of Song objects
        """
        added = 0
        for song in songs:
            if self.add_song(song):
                added += 1
        return added
    
    def remove_song(self, song_id):
        """
        Remove a song by ID.
        
        Args:
            song_id (str): ID of song to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        for i, song in enumerate(self.__songs):
            if song.get_song_id() == song_id:
                self.__songs.pop(i)
                # Adjust current index if necessary
                if self.__current_index >= len(self.__songs) and self.__songs:
                    self.__current_index = len(self.__songs) - 1
                return True
        return False
    
    def remove_song_at_index(self, index):
        """
        Remove song at specific index.
        
        Args:
            index (int): Index to remove
            
        Returns:
            bool: True if removed
        """
        if 0 <= index < len(self.__songs):
            self.__songs.pop(index)
            # Adjust current index
            if self.__current_index >= len(self.__songs) and self.__songs:
                self.__current_index = len(self.__songs) - 1
            return True
        return False
    
    def clear(self):
        """Remove all songs from playlist."""
        self.__songs = []
        self.__current_index = 0
    
    def is_empty(self):
        """
        Check if playlist is empty.
        
        Returns:
            bool: True if no songs
        """
        return len(self.__songs) == 0
    
    # ==================== PLAYBACK NAVIGATION ====================
    
    def next_song(self):
        """
        Move to next song.
        
        Returns:
            Song: Next song or None if at end
        """
        if self.__current_index < len(self.__songs) - 1:
            self.__current_index += 1
            return self.get_current_song()
        return None
    
    def previous_song(self):
        """
        Move to previous song.
        
        Returns:
            Song: Previous song or None if at start
        """
        if self.__current_index > 0:
            self.__current_index -= 1
            return self.get_current_song()
        return None
    
    def reset_position(self):
        """Reset to first song."""
        self.__current_index = 0
    
    def has_next(self):
        """Check if there's a next song."""
        return self.__current_index < len(self.__songs) - 1
    
    def has_previous(self):
        """Check if there's a previous song."""
        return self.__current_index > 0
    
    # ==================== PLAYLIST OPERATIONS ====================
    
    def shuffle(self):
        """Shuffle the playlist songs randomly."""
        if self.__songs:
            random.shuffle(self.__songs)
            self.__current_index = 0
    
    def sort_by_title(self):
        """Sort playlist by song title."""
        self.__songs.sort(key=lambda song: song.get_title())
        self.__current_index = 0
    
    def sort_by_artist(self):
        """Sort playlist by artist name."""
        self.__songs.sort(key=lambda song: song.get_artist())
        self.__current_index = 0
    
    def sort_by_rating(self, reverse=True):
        """
        Sort playlist by song rating.
        
        Args:
            reverse (bool): True for highest first (default)
        """
        self.__songs.sort(key=lambda song: song.get_rating(), reverse=reverse)
        self.__current_index = 0
    
    def sort_by_duration(self):
        """Sort playlist by song duration."""
        self.__songs.sort(key=lambda song: song.get_duration())
        self.__current_index = 0
    
    # ==================== SEARCH & FILTER ====================
    
    def find_song_by_title(self, title):
        """
        Find songs by title (partial match).
        
        Args:
            title (str): Title to search
            
        Returns:
            list: Matching songs
        """
        title_lower = title.lower()
        return [
            song for song in self.__songs
            if title_lower in song.get_title().lower()
        ]
    
    def find_song_by_artist(self, artist):
        """
        Find songs by artist (partial match).
        
        Args:
            artist (str): Artist to search
            
        Returns:
            list: Matching songs
        """
        artist_lower = artist.lower()
        return [
            song for song in self.__songs
            if artist_lower in song.get_artist().lower()
        ]
    
    def get_songs_by_mood(self, mood_tag):
        """
        Get songs matching a mood tag.
        
        Args:
            mood_tag (str): Mood to filter
            
        Returns:
            list: Matching songs
        """
        return [
            song for song in self.__songs
            if song.matches_mood_tag(mood_tag)
        ]
    
    # ==================== STATISTICS ====================
    
    def get_total_duration(self):
        """
        Calculate total duration of all songs.
        
        Returns:
            int: Total duration in seconds
        """
        return sum(song.get_duration() for song in self.__songs)
    
    def get_total_duration_formatted(self):
        """
        Get formatted total duration.
        
        Returns:
            str: Duration as HH:MM:SS
        """
        total_seconds = self.get_total_duration()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def get_average_rating(self):
        """
        Calculate average rating of songs.
        
        Returns:
            float: Average rating or 0 if no songs
        """
        if not self.__songs:
            return 0.0
        return sum(song.get_rating() for song in self.__songs) / len(self.__songs)
    
    def get_genres(self):
        """
        Get list of unique genres in playlist.
        
        Returns:
            list: Unique genres
        """
        genres = set(song.get_genre() for song in self.__songs)
        return sorted(list(genres))
    
    def get_mood_tags(self):
        """
        Get all unique mood tags from songs.
        
        Returns:
            list: Unique mood tags
        """
        tags = set()
        for song in self.__songs:
            tags.update(song.get_mood_tags())
        return sorted(list(tags))
    
    # ==================== DATA EXPORT ====================
    
    def to_dict(self):
        """
        Convert playlist to dictionary.
        
        Returns:
            dict: Playlist data
        """
        emotion_data = None
        if self.__created_for_emotion:
            emotion_data = {
                'type': self.__created_for_emotion.get_emotion_type(),
                'intensity': self.__created_for_emotion.get_intensity()
            }
        
        return {
            'playlist_id': self.__playlist_id,
            'name': self.__name,
            'song_count': len(self.__songs),
            'songs': [song.to_dict() for song in self.__songs],
            'created_for_emotion': emotion_data,
            'created_at': self.__created_at.isoformat(),
            'total_duration': self.get_total_duration(),
            'total_duration_formatted': self.get_total_duration_formatted(),
            'average_rating': round(self.get_average_rating(), 2),
            'genres': self.get_genres()
        }
    
    # ==================== STRING REPRESENTATION ====================
    
    def __str__(self):
        """String representation."""
        emotion_str = ""
        if self.__created_for_emotion:
            emotion_str = f" (for {self.__created_for_emotion.get_emotion_type()})"
        return f"Playlist: {self.__name}{emotion_str} - {len(self.__songs)} songs"
    
    def __repr__(self):
        """Debug representation."""
        return f"Playlist(id='{self.__playlist_id}', name='{self.__name}', songs={len(self.__songs)})"
    
    def __len__(self):
        """Support len() function."""
        return len(self.__songs)
    
    def __iter__(self):
        """Support iteration over songs."""
        return iter(self.__songs)


# ==================== TESTING ====================
if __name__ == "__main__":
    print("Testing Playlist Class...")
    print("=" * 60)
    
    # Create test playlist
    playlist = Playlist("pl_001", "My Happy Playlist")
    
    print("\n--- Basic Info ---")
    print(f"Playlist: {playlist}")
    print(f"ID: {playlist.get_playlist_id()}")
    print(f"Name: {playlist.get_name()}")
    print(f"Empty: {playlist.is_empty()}")
    
    # Create dummy songs
    class DummySong:
        def __init__(self, id, title, artist, rating=3.0):
            self.id = id
            self.title = title
            self.artist = artist
            self.rating = rating
        def get_song_id(self): return self.id
        def get_title(self): return self.title
        def get_artist(self): return self.artist
        def get_rating(self): return self.rating
        def get_duration(self): return 180
        def get_genre(self): return "Pop"
        def get_mood_tags(self): return ['happy']
        def matches_mood_tag(self, tag): return tag == 'happy'
        def to_dict(self): return {'id': self.id, 'title': self.title}
    
    # Add songs
    print("\n--- Adding Songs ---")
    song1 = DummySong("s1", "Happy Song 1", "Artist A", 4.5)
    song2 = DummySong("s2", "Happy Song 2", "Artist B", 4.0)
    song3 = DummySong("s3", "Happy Song 3", "Artist C", 3.5)
    
    playlist.add_song(song1)
    playlist.add_song(song2)
    playlist.add_song(song3)
    
    print(f"Songs added: {playlist.get_song_count()}")
    print(f"Current song: {playlist.get_current_song().get_title()}")
    
    # Test navigation
    print("\n--- Navigation ---")
    print(f"Has next: {playlist.has_next()}")
    next_song = playlist.next_song()
    print(f"Next song: {next_song.get_title() if next_song else 'None'}")
    print(f"Current index: {playlist.get_current_index()}")
    
    # Test statistics
    print("\n--- Statistics ---")
    print(f"Total duration: {playlist.get_total_duration_formatted()}")
    print(f"Average rating: {playlist.get_average_rating():.2f}")
    print(f"Genres: {playlist.get_genres()}")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")