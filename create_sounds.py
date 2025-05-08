import numpy as np
import soundfile as sf
import os

def create_shoot_sound():
    # Create a simple laser sound
    duration = 0.1  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a frequency sweep
    freq = np.linspace(1000, 500, len(t))
    sound = 0.5 * np.sin(2 * np.pi * freq * t)
    
    # Add a quick fade out
    sound *= np.linspace(1, 0, len(t))
    
    # Save the sound
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
    sf.write('sounds/shoot.wav', sound, sample_rate)

def create_enemy_shoot_sound():
    # Create a different laser sound for enemies
    duration = 0.15  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a lower frequency sweep
    freq = np.linspace(800, 300, len(t))
    sound = 0.5 * np.sin(2 * np.pi * freq * t)
    
    # Add a quick fade out
    sound *= np.linspace(1, 0, len(t))
    
    # Save the sound
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
    sf.write('sounds/enemy_shoot.wav', sound, sample_rate)

def create_powerup_sound():
    # Create a power-up sound
    duration = 0.3  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a rising tone with harmonics
    freq = np.linspace(300, 800, len(t))
    sound = 0.3 * np.sin(2 * np.pi * freq * t) + \
            0.2 * np.sin(4 * np.pi * freq * t) + \
            0.1 * np.sin(6 * np.pi * freq * t)
    
    # Add a quick fade in and out
    fade_in = np.linspace(0, 1, int(0.1 * sample_rate))
    fade_out = np.linspace(1, 0, int(0.2 * sample_rate))
    fade = np.concatenate([fade_in, np.ones(len(t) - len(fade_in) - len(fade_out)), fade_out])
    sound *= fade
    
    # Save the sound
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
    sf.write('sounds/powerup.wav', sound, sample_rate)

if __name__ == '__main__':
    create_shoot_sound()
    create_enemy_shoot_sound()
    create_powerup_sound() 