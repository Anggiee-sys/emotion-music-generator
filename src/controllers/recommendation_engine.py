class RecommendationEngine:
    def recommend_for_emotion(self, emotion, song_database):
        # Base method
        pass

# Inheritance + Polymorphism
class RuleBasedRecommender(RecommendationEngine):
    def recommend_for_emotion(self, emotion, song_database):
        # Override: implementasi berbeda
        # Filter songs by mood tags
        recommended = []
        for song in song_database:
            if emotion.get_type() in song.get_mood_tags():
                recommended.append(song)
        return recommended

class SmartRecommender(RecommendationEngine):
    def recommend_for_emotion(self, emotion, song_database):
        # Override: algoritma lebih pintar
        # Pertimbangkan history, preferensi, dll
        pass