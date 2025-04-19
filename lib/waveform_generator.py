import numpy as np
from constants import *

def bit_string(text):
    return ''.join(f'{ord(char):08b}'[::-1] for char in text)

def generate_resampled_tone(freq, amplitude=AMPLITUDE):
    samples_per_cycle = SAMPLE_RATE / freq
    t = np.arange(SAMPLES_PER_BIT) / SAMPLES_PER_BIT
    wave = amplitude * np.sin(2 * np.pi * t * SAMPLES_PER_BIT / samples_per_cycle)
    return wave.astype(np.int16)

TONE_MARK = generate_resampled_tone(MARK_FREQ)
TONE_SPACE = generate_resampled_tone(SPACE_FREQ)

def generate_waveform(bits):
    return np.concatenate([
        TONE_MARK if bit == '1' else TONE_SPACE
        for bit in bits
    ])

def build_same_message(header_text, repeat=3):
    preamble_bits = ''.join(f'{b:08b}'[::-1] for b in PREAMBLE_BYTES)
    header_bits = bit_string(header_text)
    full_bits = preamble_bits + header_bits
    message = []
    for _ in range(repeat):
        message.append(generate_waveform(full_bits))
        message.append(np.zeros(int(SAMPLE_RATE * 1.0), dtype=np.int16))
    return np.concatenate(message)

def build_eom(repeat=3):
    eom_bits = ''.join(f'{b:08b}'[::-1] for b in PREAMBLE_BYTES) + bit_string("NNNN")
    parts = []
    for _ in range(repeat):
        parts.append(generate_waveform(eom_bits))
        parts.append(np.zeros(int(SAMPLE_RATE * 1.0), dtype=np.int16))
    return np.concatenate(parts)

def generate_attention_tone(duration_sec, sample_rate=SAMPLE_RATE):
    num_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, num_samples, endpoint=False)
    tone1 = np.sin(2 * np.pi * ATTENTION_TONE_FREQ1 * t)
    tone2 = np.sin(2 * np.pi * ATTENTION_TONE_FREQ2 * t)
    combined = (tone1 + tone2) / 2
    return np.int16(combined * AMPLITUDE)