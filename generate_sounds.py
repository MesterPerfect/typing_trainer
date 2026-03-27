import wave
import struct
import math
import os

def generate_tone(filename: str, frequency: float, duration: float, volume: float = 0.5):
    """ Generates a standard 16-bit PCM WAV file with a sine wave tone. """
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            # Apply a simple envelope to prevent audio clicking at start/end
            envelope = 1.0
            if i < 400:
                envelope = i / 400.0
            elif i > num_samples - 400:
                envelope = (num_samples - i) / 400.0
                
            value = int(volume * envelope * 32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            wav_file.writeframes(struct.pack('<h', value))

if __name__ == "__main__":
    print("Generating sound files...")
    # Short high-pitched beep for correct typing
    generate_tone("assets/sounds/correct.wav", 800.0, 0.08, 0.3)
    
    # Low-pitched buzz for errors
    generate_tone("assets/sounds/error.wav", 150.0, 0.25, 0.4)
    
    # Higher longer chime for completion
    generate_tone("assets/sounds/complete.wav", 1200.0, 0.4, 0.3)
    
    print("Done! Valid WAV files created in assets/sounds/")
