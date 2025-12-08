"""
Emotion Class - Model for user emotions/moods

This class demonstrates:
- ENCAPSULATION: Private attributes with getters/setters
- INHERITANCE: Base class with subclasses (BasicEmotion, ComplexEmotion)

Author: [Nama Kamu]
Date: December 2025
"""

from datetime import datetime


class Emotion:
    """
    Base class for representing user emotions/moods.
    This is a parent class that can be inherited.
    
    Attributes:
        __emotion_id (str): Unique identifier
        __emotion_type (str): Type of emotion (happy, sad, calm, energetic, stressed, etc.)
        __intensity (int): Intensity level (1-10)
        __timestamp (datetime): When emotion was recorded
        __description (str): Optional text description
    """
    
    # Class variable - shared by all instances
    VALID_EMOTIONS = [
        'happy', 'sad', 'calm', 'energetic', 'stressed', 
        'anxious', 'angry', 'bored', 'tired', 'motivated',
        'relaxed', 'excited', 'melancholic', 'peaceful', 'joyful'
    ]
    
    def __init__(self, emotion_id, emotion_type, intensity, description=""):
        """
        Initialize Emotion object.
        
        Args:
            emotion_id (str): Unique identifier
            emotion_type (str): Type of emotion
            intensity (int): Intensity level (1-10)
            description (str, optional): Text description
        """
        # ENCAPSULATION: Private attributes
        self.__emotion_id = emotion_id
        self.__emotion_type = emotion_type.lower()
        self.__intensity = self._validate_intensity(intensity)
        self.__timestamp = datetime.now()
        self.__description = description
    
    # ==================== PRIVATE METHODS ====================
    
    def _validate_intensity(self, intensity):
        """
        Private method to validate intensity value.
        
        Args:
            intensity (int): Intensity to validate
            
        Returns:
            int: Validated intensity (1-10)
        """
        try:
            intensity = int(intensity)
            if 1 <= intensity <= 10:
                return intensity
            else:
                return 5  # Default to medium
        except:
            return 5
    
    # ==================== GETTER METHODS ====================
    
    def get_emotion_id(self):
        """Get emotion ID."""
        return self.__emotion_id
    
    def get_emotion_type(self):
        """Get emotion type."""
        return self.__emotion_type
    
    def get_intensity(self):
        """Get intensity level."""
        return self.__intensity
    
    def get_timestamp(self):
        """Get timestamp when emotion was recorded."""
        return self.__timestamp
    
    def get_description(self):
        """Get emotion description."""
        return self.__description
    
    # ==================== SETTER METHODS ====================
    
    def set_intensity(self, intensity):
        """
        Set intensity with validation.
        
        Args:
            intensity (int): New intensity (1-10)
        """
        self.__intensity = self._validate_intensity(intensity)
    
    def set_description(self, description):
        """
        Set emotion description.
        
        Args:
            description (str): Description text
        """
        self.__description = description
    
    # ==================== BUSINESS LOGIC ====================
    
    def matches_mood_tag(self, tag):
        """
        Check if this emotion matches a mood tag.
        
        Args:
            tag (str): Mood tag to check
            
        Returns:
            bool: True if matches
        """
        tag = tag.lower()
        emotion = self.__emotion_type.lower()
        
        # Direct match
        if tag == emotion:
            return True
        
        # Synonym matching
        synonyms = {
            'happy': ['joyful', 'cheerful', 'upbeat', 'positive'],
            'sad': ['melancholic', 'emotional', 'heartbreak', 'lonely', 'grief'],
            'calm': ['relaxed', 'peaceful', 'meditation', 'sleep', 'focus'],
            'energetic': ['motivated', 'active', 'workout', 'exercise', 'pump'],
            'stressed': ['anxious', 'tense', 'worried'],
            'tired': ['exhausted', 'sleepy', 'drowsy'],
            'angry': ['frustrated', 'irritated', 'mad'],
            'bored': ['uninterested', 'dull']
        }
        
        # Check if tag is synonym of emotion
        if emotion in synonyms:
            if tag in synonyms[emotion]:
                return True
        
        # Check if emotion is synonym of tag
        for key, values in synonyms.items():
            if tag == key and emotion in values:
                return True
        
        return False
    
    def to_mood_tags(self):
        """
        Convert emotion to list of mood tags.
        
        Returns:
            list: List of mood tags
        """
        tags = [self.__emotion_type]
        
        # Add intensity-based tags
        if self.__intensity >= 8:
            tags.append('intense')
        elif self.__intensity >= 5:
            tags.append('moderate')
        else:
            tags.append('mild')
        
        return tags
    
    def get_intensity_label(self):
        """
        Get human-readable intensity label.
        
        Returns:
            str: Intensity label
        """
        if self.__intensity >= 8:
            return "Very Strong"
        elif self.__intensity >= 6:
            return "Strong"
        elif self.__intensity >= 4:
            return "Moderate"
        else:
            return "Mild"
    
    def to_dict(self):
        """
        Convert to dictionary for JSON serialization.
        
        Returns:
            dict: Emotion data
        """
        return {
            'emotion_id': self.__emotion_id,
            'emotion_type': self.__emotion_type,
            'intensity': self.__intensity,
            'intensity_label': self.get_intensity_label(),
            'timestamp': self.__timestamp.isoformat(),
            'description': self.__description
        }
    
    def __str__(self):
        """String representation."""
        return f"{self.__emotion_type.capitalize()} (Intensity: {self.__intensity}/10)"
    
    def __repr__(self):
        """Debug representation."""
        return f"Emotion(type='{self.__emotion_type}', intensity={self.__intensity})"


# ==================== INHERITANCE: SUBCLASSES ====================

class BasicEmotion(Emotion):
    """
    INHERITANCE EXAMPLE: BasicEmotion extends Emotion
    
    Represents a simple, single emotion without complexity.
    This is a child class that inherits from Emotion parent class.
    """
    
    def __init__(self, emotion_id, emotion_type, intensity, description=""):
        """
        Initialize BasicEmotion by calling parent constructor.
        
        Args:
            emotion_id (str): Unique identifier
            emotion_type (str): Single emotion type
            intensity (int): Intensity (1-10)
            description (str): Description
        """
        # Call parent class constructor
        super().__init__(emotion_id, emotion_type, intensity, description)
        self.__is_complex = False
    
    def is_complex(self):
        """Check if emotion is complex."""
        return False
    
    def get_primary_emotion(self):
        """Get primary emotion (same as emotion_type for basic)."""
        return self.get_emotion_type()


class ComplexEmotion(Emotion):
    """
    INHERITANCE EXAMPLE: ComplexEmotion extends Emotion
    
    Represents a mixed/complex emotion (e.g., happy but anxious).
    Demonstrates inheritance with additional attributes.
    """
    
    def __init__(self, emotion_id, primary_emotion, secondary_emotion, 
                 primary_intensity, secondary_intensity, description=""):
        """
        Initialize ComplexEmotion with two emotions.
        
        Args:
            emotion_id (str): Unique identifier
            primary_emotion (str): Main emotion
            secondary_emotion (str): Secondary emotion
            primary_intensity (int): Intensity of primary (1-10)
            secondary_intensity (int): Intensity of secondary (1-10)
            description (str): Description
        """
        # Call parent with primary emotion
        super().__init__(emotion_id, primary_emotion, primary_intensity, description)
        
        # Additional attributes for complex emotion
        self.__secondary_emotion = secondary_emotion.lower()
        self.__secondary_intensity = self._validate_intensity(secondary_intensity)
    
    def get_secondary_emotion(self):
        """Get secondary emotion type."""
        return self.__secondary_emotion
    
    def get_secondary_intensity(self):
        """Get secondary emotion intensity."""
        return self.__secondary_intensity
    
    def is_complex(self):
        """Check if emotion is complex."""
        return True
    
    def get_primary_emotion(self):
        """Get primary emotion."""
        return self.get_emotion_type()
    
    def blend_emotions(self):
        """
        Create a blended emotion description.
        
        Returns:
            str: Blended description
        """
        primary = self.get_emotion_type()
        secondary = self.__secondary_emotion
        
        return f"{primary} with {secondary}"
    
    def to_mood_tags(self):
        """
        Override parent method to include both emotions.
        
        Returns:
            list: Extended mood tags
        """
        # Get tags from parent
        tags = super().to_mood_tags()
        
        # Add secondary emotion
        tags.append(self.__secondary_emotion)
        
        return tags
    
    def to_dict(self):
        """
        Override to include secondary emotion data.
        
        Returns:
            dict: Complete emotion data
        """
        data = super().to_dict()
        data['secondary_emotion'] = self.__secondary_emotion
        data['secondary_intensity'] = self.__secondary_intensity
        data['is_complex'] = True
        data['blended'] = self.blend_emotions()
        return data
    
    def __str__(self):
        """Override string representation."""
        return f"{self.get_emotion_type().capitalize()} + {self.__secondary_emotion.capitalize()}"


# ==================== TESTING ====================
if __name__ == "__main__":
    print("Testing Emotion Classes...")
    print("=" * 60)
    
    # Test BasicEmotion
    print("\n--- Testing BasicEmotion (INHERITANCE) ---")
    basic = BasicEmotion("emo_001", "happy", 8, "Feeling great today!")
    print(f"Basic Emotion: {basic}")
    print(f"Type: {basic.get_emotion_type()}")
    print(f"Intensity: {basic.get_intensity()} ({basic.get_intensity_label()})")
    print(f"Is Complex: {basic.is_complex()}")
    print(f"Mood Tags: {basic.to_mood_tags()}")
    print(f"Matches 'joyful': {basic.matches_mood_tag('joyful')}")
    
    # Test ComplexEmotion
    print("\n--- Testing ComplexEmotion (INHERITANCE) ---")
    complex_emo = ComplexEmotion(
        "emo_002", 
        "happy", 
        "anxious",
        7,
        5,
        "Happy but worried about exam"
    )
    print(f"Complex Emotion: {complex_emo}")
    print(f"Primary: {complex_emo.get_primary_emotion()} (Intensity: {complex_emo.get_intensity()})")
    print(f"Secondary: {complex_emo.get_secondary_emotion()} (Intensity: {complex_emo.get_secondary_intensity()})")
    print(f"Is Complex: {complex_emo.is_complex()}")
    print(f"Blended: {complex_emo.blend_emotions()}")
    print(f"Mood Tags: {complex_emo.to_mood_tags()}")
    
    # Test to_dict
    print("\n--- Testing Dictionary Conversion ---")
    print("Basic Dict:", basic.to_dict())
    print("\nComplex Dict:", complex_emo.to_dict())
    
    # Test class variables
    print("\n--- Testing Class Variables ---")
    print(f"Valid Emotions: {Emotion.VALID_EMOTIONS[:5]}... ({len(Emotion.VALID_EMOTIONS)} total)")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")