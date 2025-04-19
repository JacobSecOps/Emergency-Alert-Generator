from gtts import gTTS
from pydub import AudioSegment
import io
import numpy as np
from lib.logger import *

def generate_tts_message(message, target_sample_rate=96000):
    info("Generating TTS Message...")
    tts = gTTS(text=message, lang='en')
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)

    speech = AudioSegment.from_file(buffer, format="mp3")
    speech = speech.set_frame_rate(target_sample_rate).set_channels(1).set_sample_width(2)

    samples = np.frombuffer(speech.raw_data, dtype=np.int16)
    return samples