import os
import logging
import whisper
from pydub import AudioSegment
import time
import warnings

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
warnings.filterwarnings("ignore", message="You are using `torch.load` with `weights_only=False`")

# Logging Configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()

# Constants and Global Variables
TRANSCRIPTS_FOLDER = 'transcripts'
os.makedirs(TRANSCRIPTS_FOLDER, exist_ok=True)

def split_audio(file_path, chunk_length_ms=15000):
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def transcribe_file(file_path):
    model = whisper.load_model("base")  # Changed from "base" to "tiny"
    audio_chunks = split_audio(file_path)
    total_chunks = len(audio_chunks)
    
    # Create transcript file
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    transcript_filename = f"{base_filename}_transcript.txt"
    transcript_path = os.path.join(TRANSCRIPTS_FOLDER, transcript_filename)
    
    start_time = time.time()
    with open(transcript_path, 'w', encoding='utf-8') as transcript_file:
        for i, chunk in enumerate(audio_chunks):
            chunk_file = f"{file_path}_chunk_{i}.wav"
            chunk.export(chunk_file, format="wav")
            result = model.transcribe(chunk_file)
            chunk_transcript = result.get("text", "")
            
            # Append chunk transcript to file
            transcript_file.write(chunk_transcript + "\n")
            transcript_file.flush()  # Ensure writing to disk
            
            # Delete the chunk file after processing
            os.remove(chunk_file)
            logging.debug(f"Deleted chunk file: {chunk_file}")
            
            elapsed_time = time.time() - start_time
            remaining_time = elapsed_time * (total_chunks - i - 1) / (i + 1)
            logging.debug(f"Chunk {i+1}/{total_chunks} transcribed. Transcript so far: {chunk_transcript}")
            print(f"Processing chunk {i+1}/{total_chunks} ({elapsed_time:.2f}s elapsed, {remaining_time:.2f}s remaining)")
    
    print(f"Transcription complete. Transcript saved to {transcript_path}")
    return transcript_path
