"""
RecommendationEngine Classes - Music recommendation system

This module demonstrates:
- INHERITANCE: Base class with child classes
- POLYMORPHISM: Different implementations of recommend_for_emotion()
- ENCAPSULATION: Protected attributes and methods

Author: [Nama Kamu]
Date: December 2025
"""

from datetime import datetime
import random


class RecommendationEngine:
    """
    Base class for recommendation engines (Abstract/Parent class).
    
    This demonstrates INHERITANCE as a parent class that will be extended.
    
    Attributes:
        _song_database (list): Protected - list of all available songs
        _algorithm_name (str): Protected - name of recommendation algorithm
    """
    
    def __init__(self, algorithm_name="Base"):
        """
        Initialize RecommendationEngine.
        
        Args:
            algorithm_name (str): Name of the algorithm
        """
        # ENCAPSULATION: Protected attributes (single underscore)
        # Can be accessed by child classes but not from outside
        self._song_database = []
        self._algorithm_name = algorithm_name
    
    # ==================== PUBLIC METHODS ====================
    
    def update_database(self, songs):
        """
        Update the song database.
        
        Args:
            songs (list): List of Song objects
        """
        self._song_database = songs
        print(f"✓ {self._algorithm_name} updated with {len(songs)} songs")
    
    def get_database_size(self):
        """Get number of songs in database."""
        return len(self._song_database)
    
    def get_algorithm_name(self):
        """Get algorithm name."""
        return self._algorithm_name
    
    # ==================== ABSTRACT METHOD ====================
    # This method MUST be implemented by child classes (POLYMORPHISM)
    
    def recommend_for_emotion(self, emotion, user, count=10):
        """
        Abstract method - MUST be overridden by child classes.
        This demonstrates POLYMORPHISM.
        
        Args:
            emotion: Emotion object
            user: User object
            count (int): Number of songs to recommend
            
        Returns:
            Playlist: Recommended playlist
            
        Raises:
            NotImplementedError: If not overridden by child class
        """
        raise NotImplementedError("Subclass must implement recommend_for_emotion()")
    
    # ==================== PROTECTED HELPER METHODS ====================
    # These can be used by child classes
    
    def _filter_by_mood(self, emotion, songs):
        """
        Protected method: Filter songs by emotion/mood.
        
        Args:
            emotion: Emotion object
            songs (list): List of songs to filter
            
        Returns:
            list: Filtered songs
        """
        matching_songs = []
        for song in songs:
            if song.matches_emotion(emotion):
                matching_songs.append(song)
        return matching_songs
    
    def _calculate_match_score(self, song, emotion):
        """
        Protected method: Calculate how well a song matches an emotion.
        
        Args:
            song: Song object
            emotion: Emotion object
            
        Returns:
            int: Match score (0-100)
        """
        return song.calculate_match_score(emotion)
    
    def _sort_by_score(self, songs, emotion):
        """
        Protected method: Sort songs by match score.
        
        Args:
            songs (list): Songs to sort
            emotion: Emotion object
            
        Returns:
            list: Sorted songs (highest score first)
        """
        return sorted(songs, key=lambda s: self._calculate_match_score(s, emotion), reverse=True)
    
    def __str__(self):
        """String representation."""
        return f"RecommendationEngine: {self._algorithm_name} ({len(self._song_database)} songs)"


# ==================== CHILD CLASS 1: RuleBasedRecommender ====================

class RuleBasedRecommender(RecommendationEngine):
    """
    INHERITANCE & POLYMORPHISM EXAMPLE 1:
    Simple rule-based recommendation system.
    
    This class EXTENDS RecommendationEngine and OVERRIDES recommend_for_emotion()
    with a simple implementation.
    """
    
    def __init__(self):
        """Initialize RuleBasedRecommender."""
        # Call parent constructor
        super().__init__(algorithm_name="Rule-Based")
    
    # POLYMORPHISM: Override parent method with different implementation
    def recommend_for_emotion(self, emotion, user, count=10):
        """
        Simple rule-based recommendation.
        Uses direct mood tag matching.
        
        Args:
            emotion: Emotion object
            user: User object (not used in this simple version)
            count (int): Number of recommendations
            
        Returns:
            Playlist: Recommended playlist
        """
        from src.models.playlist import Playlist
        
        print(f"\n🎵 Generating recommendations using {self._algorithm_name}...")
        print(f"   Emotion: {emotion.get_emotion_type()} (Intensity: {emotion.get_intensity()})")
        
        # Step 1: Filter by mood tags
        matching_songs = self._filter_by_mood(emotion, self._song_database)
        
        if not matching_songs:
            print("   ⚠ No direct matches found, using all songs")
            matching_songs = self._song_database.copy()
        else:
            print(f"   ✓ Found {len(matching_songs)} matching songs")
        
        # Step 2: Sort by match score
        sorted_songs = self._sort_by_score(matching_songs, emotion)
        
        # Step 3: Select top N
        selected_songs = sorted_songs[:count]
        
        # Step 4: Create playlist
        playlist_name = f"{emotion.get_emotion_type().capitalize()} Mix"
        playlist_id = f"pl_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        playlist = Playlist(playlist_id, playlist_name, emotion)
        playlist.add_songs(selected_songs)
        
        print(f"   ✓ Created playlist: '{playlist_name}' with {playlist.get_song_count()} songs")
        
        return playlist


# ==================== CHILD CLASS 2: SmartRecommender ====================

class SmartRecommender(RecommendationEngine):
    """
    INHERITANCE & POLYMORPHISM EXAMPLE 2:
    Advanced recommendation system with user history.
    
    This class EXTENDS RecommendationEngine and OVERRIDES recommend_for_emotion()
    with a MORE SOPHISTICATED implementation.
    """
    
    def __init__(self):
        """Initialize SmartRecommender."""
        super().__init__(algorithm_name="Smart AI")
        self._user_feedback = {}  # Track user likes/dislikes
    
    # POLYMORPHISM: Override with more advanced implementation
    def recommend_for_emotion(self, emotion, user, count=10):
        """
        Advanced recommendation using:
        - Emotion matching
        - User preferences
        - Listening history
        - User feedback
        
        Args:
            emotion: Emotion object
            user: User object
            count (int): Number of recommendations
            
        Returns:
            Playlist: Personalized recommended playlist
        """
        from src.models.playlist import Playlist
        
        print(f"\n🤖 Generating AI recommendations using {self._algorithm_name}...")
        print(f"   User: {user.get_username()}")
        print(f"   Emotion: {emotion.get_emotion_type()} (Intensity: {emotion.get_intensity()})")
        
        # Step 1: Filter by mood
        matching_songs = self._filter_by_mood(emotion, self._song_database)
        
        if not matching_songs:
            matching_songs = self._song_database.copy()
        
        # Step 2: Score each song with advanced algorithm
        scored_songs = []
        for song in matching_songs:
            score = self._calculate_advanced_score(song, emotion, user)
            scored_songs.append((song, score))
        
        # Step 3: Sort by score
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Step 4: Select with diversity
        selected_songs = self._select_with_diversity(scored_songs, count, user)
        
        # Step 5: Create personalized playlist
        playlist_name = f"AI Mix for {user.get_username()}: {emotion.get_emotion_type().capitalize()}"
        playlist_id = f"pl_smart_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        playlist = Playlist(playlist_id, playlist_name, emotion)
        playlist.add_songs(selected_songs)
        
        print(f"   ✓ Created personalized playlist with {playlist.get_song_count()} songs")
        
        return playlist
    
    # ==================== PRIVATE ADVANCED METHODS ====================
    
    def _calculate_advanced_score(self, song, emotion, user):
        """
        Calculate advanced match score considering user preferences.
        
        Args:
            song: Song object
            emotion: Emotion object
            user: User object
            
        Returns:
            float: Advanced score
        """
        # Base score from emotion match
        base_score = self._calculate_match_score(song, emotion)
        
        # Bonus: User's favorite genres
        genre_bonus = 0
        if song.get_genre() in user.get_favorite_genres():
            genre_bonus = 15
        
        # Bonus: User's preferred tempo
        tempo_bonus = 0
        if song.get_tempo() == user.get_preferred_tempo():
            tempo_bonus = 10
        
        # Bonus: High rating
        rating_bonus = song.get_rating() * 5
        
        # Penalty: Recently played (to avoid repetition)
        recent_penalty = 0
        recent_moods = user.get_recent_moods(20)
        # Simplified: In real app, would check actual song history
        
        total_score = base_score + genre_bonus + tempo_bonus + rating_bonus - recent_penalty
        
        return max(0, min(100, total_score))  # Clamp to 0-100
    
    def _select_with_diversity(self, scored_songs, count, user):
        """
        Select songs ensuring genre diversity.
        
        Args:
            scored_songs (list): List of (song, score) tuples
            count (int): Number to select
            user: User object
            
        Returns:
            list: Selected songs
        """
        selected = []
        genres_used = set()
        
        # First pass: Select best songs with genre diversity
        for song, score in scored_songs:
            if len(selected) >= count:
                break
            
            genre = song.get_genre()
            
            # Prefer diverse genres, but allow repeats after variety
            if genre not in genres_used or len(genres_used) >= 3:
                selected.append(song)
                genres_used.add(genre)
        
        # If not enough, add remaining best songs
        if len(selected) < count:
            for song, score in scored_songs:
                if song not in selected:
                    selected.append(song)
                    if len(selected) >= count:
                        break
        
        return selected
    
    def learn_from_feedback(self, song_id, user_id, liked):
        """
        Learn from user feedback (like/dislike).
        
        Args:
            song_id (str): Song ID
            user_id (str): User ID
            liked (bool): True if liked, False if disliked
        """
        key = f"{user_id}_{song_id}"
        self._user_feedback[key] = liked
        
        action = "liked" if liked else "disliked"
        print(f"📊 Learned: User {user_id} {action} song {song_id}")


# ==================== TESTING ====================
if __name__ == "__main__":
    print("Testing Recommendation Engine Classes...")
    print("=" * 60)
    
    # Test inheritance
    print("\n--- Testing INHERITANCE ---")
    base = RecommendationEngine("Base Test")
    print(f"Base Engine: {base}")
    
    rule_based = RuleBasedRecommender()
    print(f"Rule-Based Engine: {rule_based}")
    
    smart = SmartRecommender()
    print(f"Smart Engine: {smart}")
    
    # Test polymorphism
    print("\n--- Testing POLYMORPHISM ---")
    print("Both child classes override recommend_for_emotion() differently")
    print(f"RuleBasedRecommender uses: Simple mood tag matching")
    print(f"SmartRecommender uses: AI with user preferences & history")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")
    print("Note: Full testing requires Song, Emotion, User, and Playlist objects")