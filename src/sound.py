import os
import pygame

class Sound:
    def __init__(self, relative_path):
        base_dir = os.path.dirname(os.path.dirname(__file__))  # AI-Chess/
        full_path = os.path.join(base_dir, relative_path)
        self.sound = pygame.mixer.Sound(full_path)

    def play(self):
        self.sound.play()
