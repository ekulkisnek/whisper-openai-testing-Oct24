import os
import whisper
from pydub import AudioSegment
import time

TRANSCRIPTS_FOLDER = 'transcripts'
os.makedirs(TRANSCRIPTS_FOLDER, exist_ok=True)

MODEL = whisper.load_model("base")

def split_audio(file_path, chunk_length_ms=15000):
    audio = AudioSegment.from_file(file_path)
    return [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

def transcribe_file(file_path):
    audio_chunks = split_audio(file_path)
    total_chunks = len(audio_chunks)
    
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    transcript_filename = f"{base_filename}_transcript.txt"
    transcript_path = os.path.join(TRANSCRIPTS_FOLDER, transcript_filename)
    
    start_time = time.time()
    with open(transcript_path, 'w', encoding='utf-8') as transcript_file:
        for i, chunk in enumerate(audio_chunks):
            chunk_file = f"{file_path}_chunk_{i}.wav"
            chunk.export(chunk_file, format="wav")
            result = MODEL.transcribe(chunk_file)
            chunk_transcript = result.get("text", "")
            
            transcript_file.write(chunk_transcript + "\n")
            transcript_file.flush()
            
            os.remove(chunk_file)
            
            elapsed_time = time.time() - start_time
            remaining_time = elapsed_time * (total_chunks - i - 1) / (i + 1)
            print(f"Processing chunk {i+1}/{total_chunks} ({elapsed_time:.2f}s elapsed, {remaining_time:.2f}s remaining)")
    
    print(f"Transcription complete. Transcript saved to {transcript_path}")
    return transcript_path
