"""
Sound Effects and Music Management
"""

import pygame
import os

class SoundManager:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.sounds = {}
        self.music_playing = False
        
        if enabled:
            self.init_audio()
    
    def init_audio(self):
        """Initialize audio system"""
        try:
            pygame.mixer.init()
            self.load_sounds()
            return True
        except:
            self.enabled = False
            return False
    
    def load_sounds(self):
        """Load sound effects"""
        sound_files = {
            'dice_roll': 'sounds/dice_roll.wav',
            'snake_bite': 'sounds/snake_bite.wav', 
            'ladder_climb': 'sounds/ladder_climb.wav',
            'win': 'sounds/win.wav',
            'move': 'sounds/move.wav'
        }
        
        for sound_name, file_path in sound_files.items():
            if os.path.exists(file_path):
                self.sounds[sound_name] = pygame.mixer.Sound(file_path)
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if self.enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, music_file):
        """Play background music"""
        if self.enabled and os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.music_playing = True
    
    def stop_music(self):
        """Stop background music"""
        if self.enabled:
            pygame.mixer.music.stop()
            self.music_playing = False
    
    def set_volume(self, volume):
        """Set volume for all sounds (0.0 to 1.0)"""
        if self.enabled:
            pygame.mixer.music.set_volume(volume)
            for sound in self.sounds.values():
                sound.set_volume(volume)