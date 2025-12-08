"""
Song Class - Model for music tracks

This class demonstrates ENCAPSULATION through:
- Private attributes (using __ prefix)
- Public getter methods
- Public setter methods with validation

Author: [Nama Kamu]
Date: December 2025
"""


class Song:
    """
    Represents a music song/track in the application.
    
    Attributes:
        __song_id (str): Unique identifier for the song
        __title (str): Song title
        __artist (str): Artist name
        __file_path (str): Path to the MP3 file
        __mood_tags (list): List of mood tags (e.g., ['happy', 'energetic'])
        __tempo (str): Tempo category ('slow', 'medium', 'fast')
        __genre (str): Music genre
        __duration (int): Song duration in seconds
        __play_count (int): Number of times played
        __rating (float): User rating (0.0 - 5.0)
    """
    
    def __init__(self, song_id, title, artist, file_path, mood_tags, tempo, genre="Unknown", duration=0):
        """
        Initialize a Song object.
        
        Args:
            song_id (str): Unique song identifier
            title (str): Song title
            artist (str): Artist name
            file_path (str): Path to MP3 file
            mood_tags (list): List of mood tags
            tempo (str): Tempo category
            genre (str, optional): Music genre. Defaults to "Unknown"
            duration (int, optional): Duration in seconds. Defaults to 0
        """
        # ENCAPSULATION: Private attributes (cannot be accessed directly)
        self.__song_id = song_id
        self.__title = title
        self.__artist = artist
        self.__file_path = file_path
        self.__mood_tags = mood_tags if mood_tags else []
        self.__tempo = tempo
        self.__genre = genre
        self.__duration = duration
        self.__play_count = 0
        self.__rating = 0.0
    
    # ==================== GETTER METHODS ====================
    # Public methods to access private attributes (ENCAPSULATION)
    
    def get_song_id(self):
        """Get song ID."""
        return self.__song_id
    
    def get_title(self):
        """Get song title."""
        return self.__title
    
    def get_artist(self):
        """Get artist name."""
        return self.__artist
    
    def get_file_path(self):
        """Get file path to MP3."""
        return self.__file_path
    
    def get_mood_tags(self):
        """Get list of mood tags."""
        return self.__mood_tags.copy()  # Return copy to prevent external modification
    
    def get_tempo(self):
        """Get tempo category."""
        return self.__tempo
    
    def get_genre(self):
        """Get music genre."""
        return self.__genre
    
    def get_duration(self):
        """Get duration in seconds."""
        return self.__duration
    
    def get_play_count(self):
        """Get number of times played."""
        return self.__play_count
    
    def get_rating(self):
        """Get user rating."""
        return self.__rating
    
    # ==================== SETTER METHODS ====================
    # Public methods to modify private attributes with validation
    
    def set_title(self, title):
        """
        Set song title with validation.
        
        Args:
            title (str): New title
        """
        if title and len(title.strip()) > 0:
            self.__title = title.strip()
        else:
            raise ValueError("Title cannot be empty")
    
    def set_artist(self, artist):
        """
        Set artist name with validation.
        
        Args:
            artist (str): New artist name
        """
        if artist and len(artist.strip()) > 0:
            self.__artist = artist.strip()
        else:
            raise ValueError("Artist name cannot be empty")
    
    def set_rating(self, rating):
        """
        Set song rating with validation.
        
        Args:
            rating (float): Rating value (0.0 - 5.0)
        """
        if 0.0 <= rating <= 5.0:
            self.__rating = float(rating)
        else:
            raise ValueError("Rating must be between 0.0 and 5.0")
    
    def add_mood_tag(self, tag):
        """
        Add a new mood tag if not already present.
        
        Args:
            tag (str): Mood tag to add
        """
        tag = tag.lower().strip()
        if tag and tag not in self.__mood_tags:
            self.__mood_tags.append(tag)
    
    def remove_mood_tag(self, tag):
        """
        Remove a mood tag.
        
        Args:
            tag (str): Mood tag to remove
        """
        tag = tag.lower().strip()
        if tag in self.__mood_tags:
            self.__mood_tags.remove(tag)
    
    # ==================== BUSINESS LOGIC METHODS ====================
    
    def increment_play_count(self):
        """
        Increment play count by 1.
        Called when song is played.
        """
        self.__play_count += 1
    
    def matches_emotion(self, emotion):
        """
        Check if this song matches a given emotion.
        
        Args:
            emotion: Emotion object with emotion_type attribute
            
        Returns:
            bool: True if song matches emotion, False otherwise
        """
        emotion_type = emotion.get_emotion_type().lower()
        return emotion_type in self.__mood_tags
    
    def matches_mood_tag(self, tag):
        """
        Check if this song has a specific mood tag.
        
        Args:
            tag (str): Mood tag to check
            
        Returns:
            bool: True if song has this tag, False otherwise
        """
        return tag.lower() in self.__mood_tags
    
    def calculate_match_score(self, emotion):
        """
        Calculate how well this song matches an emotion (0-100).
        
        Args:
            emotion: Emotion object
            
        Returns:
            int: Match score (0-100)
        """
        emotion_type = emotion.get_emotion_type().lower()
        intensity = emotion.get_intensity()
        
        score = 0
        
        # Base score: emotion type match
        if emotion_type in self.__mood_tags:
            score += 50
        
        # Bonus: intensity match with tempo
        if intensity >= 7 and self.__tempo == 'fast':
            score += 20
        elif 4 <= intensity <= 6 and self.__tempo == 'medium':
            score += 20
        elif intensity <= 3 and self.__tempo == 'slow':
            score += 20
        
        # Bonus: rating
        score += int(self.__rating * 6)  # Up to 30 points
        
        return min(score, 100)  # Cap at 100
    
    def get_duration_formatted(self):
        """
        Get duration in formatted string (MM:SS).
        
        Returns:
            str: Formatted duration
        """
        minutes = self.__duration // 60
        seconds = self.__duration % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    # ==================== STRING REPRESENTATION ====================
    
    def __str__(self):
        """
        String representation of Song object.
        
        Returns:
            str: Human-readable song info
        """
        return f"{self.__title} - {self.__artist} ({self.__genre})"
    
    def __repr__(self):
        """
        Official string representation for debugging.
        
        Returns:
            str: Detailed song info
        """
        return f"Song(id='{self.__song_id}', title='{self.__title}', artist='{self.__artist}')"
    
    def to_dict(self):
        """
        Convert Song object to dictionary (for JSON serialization).
        
        Returns:
            dict: Song data as dictionary
        """
        return {
            'song_id': self.__song_id,
            'title': self.__title,
            'artist': self.__artist,
            'file_path': self.__file_path,
            'mood_tags': self.__mood_tags,
            'tempo': self.__tempo,
            'genre': self.__genre,
            'duration': self.__duration,
            'play_count': self.__play_count,
            'rating': self.__rating
        }


# ==================== TESTING ====================
if __name__ == "__main__":
    """
    Test code - runs only when this file is executed directly.
    Not executed when imported as a module.
    """
    print("Testing Song Class...")
    print("=" * 50)
    
    # Create a test song
    song = Song(
        song_id="test_001",
        title="Test Happy Song",
        artist="Test Artist",
        file_path="assets/music/happysong1.mp3",
        mood_tags=['happy', 'joyful', 'upbeat'],
        tempo='medium',
        genre='Pop',
        duration=180
    )
    
    # Test getters
    print(f"\nTitle: {song.get_title()}")
    print(f"Artist: {song.get_artist()}")
    print(f"Genre: {song.get_genre()}")
    print(f"Duration: {song.get_duration_formatted()}")
    print(f"Mood Tags: {song.get_mood_tags()}")
    print(f"Tempo: {song.get_tempo()}")
    
    # Test setters
    print("\n--- Testing Setters ---")
    song.set_rating(4.5)
    print(f"Rating set to: {song.get_rating()}")
    
    # Test play count
    print("\n--- Testing Play Count ---")
    song.increment_play_count()
    song.increment_play_count()
    print(f"Play count: {song.get_play_count()}")
    
    # Test mood tags
    print("\n--- Testing Mood Tags ---")
    song.add_mood_tag('energetic')
    print(f"Mood tags after adding: {song.get_mood_tags()}")
    
    # Test string representation
    print("\n--- String Representation ---")
    print(f"str(): {str(song)}")
    print(f"repr(): {repr(song)}")
    
    # Test to_dict
    print("\n--- Dictionary Representation ---")
    print(song.to_dict())
    
    print("\n" + "=" * 50)
    print("✓ All tests completed!")