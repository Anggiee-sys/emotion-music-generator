import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.__current_song = None
        self.__is_playing = False
    
    def play(self, song):
        pygame.mixer.music.load(song.get_file_path())
        pygame.mixer.music.play()
        self.__is_playing = True
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def stop(self):
        pygame.mixer.music.stop()