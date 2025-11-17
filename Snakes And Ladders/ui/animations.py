"""
Advanced Animations and Visual Effects
"""

import pygame
import math
import random

class AnimationManager:
    def __init__(self, screen):
        self.screen = screen
        self.animations = []
        self.particles = []
    
    def add_dice_roll_animation(self, position, dice_value):
        """Add dice roll animation"""
        animation = {
            'type': 'dice_roll',
            'position': position,
            'dice_value': dice_value,
            'frames': 0,
            'max_frames': 30
        }
        self.animations.append(animation)
    
    def add_snake_bite_animation(self, start_pos, end_pos):
        """Add snake bite animation"""
        animation = {
            'type': 'snake_bite',
            'start_pos': start_pos,
            'end_pos': end_pos,
            'progress': 0.0,
            'duration': 60  # frames
        }
        self.animations.append(animation)
    
    def add_ladder_climb_animation(self, start_pos, end_pos):
        """Add ladder climb animation"""
        animation = {
            'type': 'ladder_climb',
            'start_pos': start_pos,
            'end_pos': end_pos,
            'progress': 0.0,
            'duration': 45  # frames
        }
        self.animations.append(animation)
    
    def add_celebration_particles(self, position, count=50):
        """Add celebration particles"""
        for _ in range(count):
            particle = {
                'position': list(position),
                'velocity': [random.uniform(-3, 3), random.uniform(-5, -2)],
                'color': random.choice([
                    (255, 255, 0), (255, 0, 0), (0, 255, 0), 
                    (0, 255, 255), (255, 0, 255)
                ]),
                'life': random.randint(30, 90),
                'size': random.randint(2, 6)
            }
            self.particles.append(particle)
    
    def update(self):
        """Update all animations"""
        # Update animations
        for animation in self.animations[:]:
            if animation['type'] == 'dice_roll':
                animation['frames'] += 1
                if animation['frames'] >= animation['max_frames']:
                    self.animations.remove(animation)
            
            elif animation['type'] in ['snake_bite', 'ladder_climb']:
                animation['progress'] += 1 / animation['duration']
                if animation['progress'] >= 1.0:
                    self.animations.remove(animation)
        
        # Update particles
        for particle in self.particles[:]:
            particle['position'][0] += particle['velocity'][0]
            particle['position'][1] += particle['velocity'][1]
            particle['velocity'][1] += 0.1  # gravity
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self):
        """Draw all animations"""
        for animation in self.animations:
            if animation['type'] == 'dice_roll':
                self._draw_dice_roll(animation)
            elif animation['type'] == 'snake_bite':
                self._draw_snake_bite(animation)
            elif animation['type'] == 'ladder_climb':
                self._draw_ladder_climb(animation)
        
        for particle in self.particles:
            pygame.draw.circle(
                self.screen,
                particle['color'],
                [int(particle['position'][0]), int(particle['position'][1])],
                particle['size']
            )
    
    def _draw_dice_roll(self, animation):
        """Draw dice roll animation"""
        x, y = animation['position']
        frames = animation['frames']
        
        # Pulsing effect
        size = 40 + 10 * math.sin(frames * 0.3)
        
        # Draw dice
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, size, size))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, size, size), 2)
        
        # Draw dots based on dice value (simplified)
        if frames > animation['max_frames'] * 0.7:
            value = animation['dice_value']
            dot_color = (0, 0, 0)
            
            # Draw center dot for odd numbers
            if value % 2 == 1:
                pygame.draw.circle(self.screen, dot_color, (x + size//2, y + size//2), 4)
    
    def _draw_snake_bite(self, animation):
        """Draw snake bite animation"""
        start_x, start_y = animation['start_pos']
        end_x, end_y = animation['end_pos']
        progress = animation['progress']
        
        # Current position along the path
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress
        
        # Draw snake body segments
        segments = 10
        for i in range(segments):
            seg_progress = progress - (i * 0.05)
            if seg_progress < 0:
                continue
            
            seg_x = start_x + (end_x - start_x) * seg_progress
            seg_y = start_y + (end_y - start_y) * seg_progress
            
            # Snake-like sine wave
            wave_offset = math.sin(seg_progress * 20) * 10
            pygame.draw.circle(self.screen, (0, 200, 0), 
                             (int(seg_x + wave_offset), int(seg_y)), 5)
        
        # Draw snake head
        pygame.draw.circle(self.screen, (255, 0, 0), (int(current_x), int(current_y)), 8)
    
    def _draw_ladder_climb(self, animation):
        """Draw ladder climb animation"""
        start_x, start_y = animation['start_pos']
        end_x, end_y = animation['end_pos']
        progress = animation['progress']
        
        # Current position
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress
        
        # Draw ladder
        ladder_width = 20
        pygame.draw.line(self.screen, (139, 69, 19), 
                        (start_x - ladder_width//2, start_y),
                        (end_x - ladder_width//2, end_y), 3)
        pygame.draw.line(self.screen, (139, 69, 19), 
                        (start_x + ladder_width//2, start_y),
                        (end_x + ladder_width//2, end_y), 3)
        
        # Draw rungs
        rungs = 8
        for i in range(rungs):
            rung_progress = i / (rungs - 1)
            rung_x1 = start_x - ladder_width//2 + (end_x - start_x) * rung_progress
            rung_y1 = start_y + (end_y - start_y) * rung_progress
            rung_x2 = start_x + ladder_width//2 + (end_x - start_x) * rung_progress
            rung_y2 = rung_y1
            
            pygame.draw.line(self.screen, (160, 82, 45), 
                           (rung_x1, rung_y1), (rung_x2, rung_y2), 2)
        
        # Draw climbing player
        pygame.draw.circle(self.screen, (255, 255, 0), (int(current_x), int(current_y)), 6)