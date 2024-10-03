import os
import logging
import openai
from pydub import AudioSegment
import time

# Logging Configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()

# Constants and Global Variables
TRANSCRIPTS_FOLDER = 'transcripts'
os.makedirs(TRANSCRIPTS_FOLDER, exist_ok=True)

# Initialize OpenAI client
openai.api_key = os.environ.get("OPENAI_API_KEY")

def save_transcript_as_txt(transcript, filename):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(TRANSCRIPTS_FOLDER, f"{timestamp}_{filename}.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(transcript)
    logging.debug(f"Transcript saved to {file_path}.")
    return file_path

def split_audio(file_path, chunk_length_ms=15000):
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def transcribe_file(file_path):
    audio_chunks = split_audio(file_path)
    total_chunks = len(audio_chunks)
    transcript = ""
    start_time = time.time()
    for i, chunk in enumerate(audio_chunks):
        chunk_file = f"{file_path}_chunk_{i}.wav"
        chunk.export(chunk_file, format="wav")
        with open(chunk_file, "rb") as audio_file:
            result = openai.Audio.transcribe("whisper-1", audio_file)
        chunk_transcript = result.get("text", "")
        transcript += chunk_transcript + "\n"
        elapsed_time = time.time() - start_time
        remaining_time = elapsed_time * (total_chunks - i - 1) / (i + 1)
        logging.debug(f"Chunk {i+1}/{total_chunks} transcribed. Transcript so far: {chunk_transcript}")
        print(f"Processing chunk {i+1}/{total_chunks} ({elapsed_time:.2f}s elapsed, {remaining_time:.2f}s remaining)")
    save_transcript_as_txt(transcript, os.path.basename(file_path))
    print("Transcription complete.")
    return transcript
