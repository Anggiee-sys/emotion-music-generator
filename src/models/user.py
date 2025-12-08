"""
User Class - Model for application users

This class demonstrates ENCAPSULATION through:
- Private attributes for user data
- Controlled access through getter/setter methods
- Private methods for internal operations

Author: [Nama Kamu]
Date: December 2025
"""

from datetime import datetime
import json


class User:
    """
    Represents a user in the Emotion-Based Music Generator.
    
    Attributes:
        __user_id (str): Unique user identifier
        __username (str): Username
        __email (str): User email
        __preferences (dict): User preferences (genres, tempo, etc.)
        __mood_history (list): List of mood records
        __created_at (datetime): Account creation timestamp
    """
    
    def __init__(self, user_id, username, email=""):
        """
        Initialize User object.
        
        Args:
            user_id (str): Unique identifier
            username (str): Username
            email (str, optional): Email address
        """
        # ENCAPSULATION: Private attributes
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__preferences = {
            'favorite_genres': [],
            'preferred_tempo': 'medium',  # slow, medium, fast
            'listening_hours': {'morning': 0, 'afternoon': 0, 'evening': 0, 'night': 0}
        }
        self.__mood_history = []
        self.__created_at = datetime.now()
    
    # ==================== GETTER METHODS ====================
    
    def get_user_id(self):
        """Get user ID."""
        return self.__user_id
    
    def get_username(self):
        """Get username."""
        return self.__username
    
    def get_email(self):
        """Get email."""
        return self.__email
    
    def get_preferences(self):
        """
        Get user preferences (returns copy to prevent external modification).
        
        Returns:
            dict: User preferences
        """
        return self.__preferences.copy()
    
    def get_mood_history(self):
        """
        Get mood history (returns copy).
        
        Returns:
            list: Mood history records
        """
        return self.__mood_history.copy()
    
    def get_created_at(self):
        """Get account creation date."""
        return self.__created_at
    
    def get_favorite_genres(self):
        """Get list of favorite genres."""
        return self.__preferences['favorite_genres'].copy()
    
    def get_preferred_tempo(self):
        """Get preferred tempo."""
        return self.__preferences['preferred_tempo']
    
    # ==================== SETTER METHODS ====================
    
    def set_username(self, username):
        """
        Set username with validation.
        
        Args:
            username (str): New username
        """
        if username and len(username.strip()) >= 3:
            self.__username = username.strip()
        else:
            raise ValueError("Username must be at least 3 characters")
    
    def set_email(self, email):
        """
        Set email with basic validation.
        
        Args:
            email (str): Email address
        """
        if '@' in email and '.' in email:
            self.__email = email.strip()
        else:
            raise ValueError("Invalid email format")
    
    def set_preferences(self, preferences):
        """
        Set user preferences.
        
        Args:
            preferences (dict): Preferences dictionary
        """
        if isinstance(preferences, dict):
            self.__preferences.update(preferences)
    
    def set_preferred_tempo(self, tempo):
        """
        Set preferred tempo.
        
        Args:
            tempo (str): Tempo preference (slow/medium/fast)
        """
        valid_tempos = ['slow', 'medium', 'fast']
        if tempo.lower() in valid_tempos:
            self.__preferences['preferred_tempo'] = tempo.lower()
        else:
            raise ValueError(f"Tempo must be one of: {valid_tempos}")
    
    # ==================== PREFERENCE MANAGEMENT ====================
    
    def add_favorite_genre(self, genre):
        """
        Add a genre to favorites.
        
        Args:
            genre (str): Genre name
        """
        genre = genre.strip().title()
        if genre and genre not in self.__preferences['favorite_genres']:
            self.__preferences['favorite_genres'].append(genre)
    
    def remove_favorite_genre(self, genre):
        """
        Remove a genre from favorites.
        
        Args:
            genre (str): Genre to remove
        """
        genre = genre.strip().title()
        if genre in self.__preferences['favorite_genres']:
            self.__preferences['favorite_genres'].remove(genre)
    
    # ==================== MOOD HISTORY MANAGEMENT ====================
    
    def record_mood(self, emotion, playlist_id=None, timestamp=None):
        """
        Record a mood entry (ENCAPSULATION: private data manipulation).
        
        Args:
            emotion: Emotion object
            playlist_id (str, optional): Playlist that was generated
            timestamp (datetime, optional): When recorded (default: now)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        mood_record = {
            'emotion_type': emotion.get_emotion_type(),
            'intensity': emotion.get_intensity(),
            'timestamp': timestamp,
            'playlist_id': playlist_id,
            'time_of_day': self._get_time_of_day(timestamp)
        }
        
        self.__mood_history.append(mood_record)
        
        # Update listening hours
        time_of_day = mood_record['time_of_day']
        self.__preferences['listening_hours'][time_of_day] += 1
    
    def get_mood_history_by_date(self, date):
        """
        Get mood records for a specific date.
        
        Args:
            date (datetime.date): Date to filter
            
        Returns:
            list: Mood records for that date
        """
        return [
            record for record in self.__mood_history
            if record['timestamp'].date() == date
        ]
    
    def get_mood_history_by_emotion(self, emotion_type):
        """
        Get all records of a specific emotion.
        
        Args:
            emotion_type (str): Emotion to filter
            
        Returns:
            list: Filtered mood records
        """
        emotion_type = emotion_type.lower()
        return [
            record for record in self.__mood_history
            if record['emotion_type'] == emotion_type
        ]
    
    def get_recent_moods(self, count=10):
        """
        Get most recent mood records.
        
        Args:
            count (int): Number of records to return
            
        Returns:
            list: Recent mood records
        """
        return self.__mood_history[-count:] if self.__mood_history else []
    
    def clear_mood_history(self):
        """Clear all mood history."""
        self.__mood_history = []
    
    # ==================== STATISTICS ====================
    
    def get_mood_statistics(self):
        """
        Calculate mood statistics.
        
        Returns:
            dict: Statistics about user's moods
        """
        if not self.__mood_history:
            return {
                'total_records': 0,
                'most_common_mood': None,
                'average_intensity': 0,
                'mood_distribution': {}
            }
        
        # Count emotions
        emotion_counts = {}
        total_intensity = 0
        
        for record in self.__mood_history:
            emotion = record['emotion_type']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            total_intensity += record['intensity']
        
        # Find most common
        most_common = max(emotion_counts.items(), key=lambda x: x[1])
        
        return {
            'total_records': len(self.__mood_history),
            'most_common_mood': most_common[0],
            'most_common_count': most_common[1],
            'average_intensity': round(total_intensity / len(self.__mood_history), 2),
            'mood_distribution': emotion_counts,
            'favorite_time': self._get_favorite_listening_time()
        }
    
    # ==================== PRIVATE HELPER METHODS ====================
    
    def _get_time_of_day(self, timestamp):
        """
        Private method to determine time of day category.
        
        Args:
            timestamp (datetime): Timestamp to categorize
            
        Returns:
            str: Time category (morning/afternoon/evening/night)
        """
        hour = timestamp.hour
        
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 21:
            return 'evening'
        else:
            return 'night'
    
    def _get_favorite_listening_time(self):
        """
        Private method to get favorite listening time.
        
        Returns:
            str: Favorite time of day
        """
        hours = self.__preferences['listening_hours']
        if sum(hours.values()) == 0:
            return 'unknown'
        return max(hours.items(), key=lambda x: x[1])[0]
    
    # ==================== DATA PERSISTENCE ====================
    
    def to_dict(self):
        """
        Convert User to dictionary for JSON serialization.
        
        Returns:
            dict: User data
        """
        return {
            'user_id': self.__user_id,
            'username': self.__username,
            'email': self.__email,
            'preferences': self.__preferences,
            'mood_history_count': len(self.__mood_history),
            'created_at': self.__created_at.isoformat(),
            'statistics': self.get_mood_statistics()
        }
    
    def save_to_file(self, filepath):
        """
        Save user data to JSON file.
        
        Args:
            filepath (str): Path to save file
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving user data: {e}")
            return False
    
    # ==================== STRING REPRESENTATION ====================
    
    def __str__(self):
        """String representation."""
        return f"User: {self.__username} (ID: {self.__user_id})"
    
    def __repr__(self):
        """Debug representation."""
        return f"User(id='{self.__user_id}', username='{self.__username}')"


# ==================== TESTING ====================
if __name__ == "__main__":
    print("Testing User Class...")
    print("=" * 60)
    
    # Create test user
    user = User("user_001", "TestUser", "test@example.com")
    
    # Test getters
    print("\n--- Basic Info ---")
    print(f"User ID: {user.get_user_id()}")
    print(f"Username: {user.get_username()}")
    print(f"Email: {user.get_email()}")
    
    # Test preferences
    print("\n--- Preferences ---")
    user.add_favorite_genre("Pop")
    user.add_favorite_genre("Rock")
    user.set_preferred_tempo("fast")
    print(f"Favorite Genres: {user.get_favorite_genres()}")
    print(f"Preferred Tempo: {user.get_preferred_tempo()}")
    
    # Test mood recording (need to create dummy Emotion)
    print("\n--- Mood Recording ---")
    
    class DummyEmotion:
        def get_emotion_type(self): return "happy"
        def get_intensity(self): return 8
    
    emotion = DummyEmotion()
    user.record_mood(emotion)
    user.record_mood(emotion)
    
    print(f"Mood History Count: {len(user.get_mood_history())}")
    print(f"Recent Moods: {user.get_recent_moods(2)}")
    
    # Test statistics
    print("\n--- Statistics ---")
    stats = user.get_mood_statistics()
    print(f"Total Records: {stats['total_records']}")
    print(f"Most Common Mood: {stats['most_common_mood']}")
    print(f"Average Intensity: {stats['average_intensity']}")
    
    # Test to_dict
    print("\n--- Dictionary Representation ---")
    print(user.to_dict())
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")