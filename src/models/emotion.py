class Emotion:
    def __init__(self, emotion_type, intensity):
        self.__emotion_type = emotion_type  # 'happy', 'sad', etc
        self.__intensity = intensity  # 1-10
    
    def matches_mood_tag(self, tag):
        # Logic untuk matching
        pass