class Song:
    def __init__(self, song_id, title, artist, file_path, mood_tags, tempo):
        self.__song_id = song_id  # Encapsulation: private
        self.__title = title
        self.__artist = artist
        self.__file_path = file_path
        self.__mood_tags = mood_tags  # ['happy', 'energetic']
        self.__tempo = tempo
    
    # Getter methods
    def get_title(self):
        return self.__title
    
    # ... dst