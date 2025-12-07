class User:
    def __init__(self, user_id, username):
        self.__user_id = user_id
        self.__username = username
        self.__preferences = {}  # genre favorit, tempo
        self.__mood_history = []
    
    def record_mood(self, emotion, timestamp):
        # Encapsulation: private method
        pass