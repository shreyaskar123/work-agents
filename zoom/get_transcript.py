import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openai import OpenAI
import openai
from docx import Document
from get_subtask_and_do_code import main

# Configure OpenAI client (ensure OPENAI_API_KEY is set in your environment variables)
client = OpenAI()

class NewFolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            return

        new_folder_path = event.src_path
        print(f"New folder detected: {new_folder_path}")
        
        # Wait a bit for files to appear
        timeout = time.time() + 600  # 10 minutes from now
        found_audio_file = False
        
        while time.time() < timeout and not found_audio_file:
            for root, dirs, files in os.walk(new_folder_path):
                for file in files:
                    if 'audio' in file and file.endswith('.m4a'):
                        audio_file_path = os.path.join(root, file)
                        print(f"Transcribing file: {audio_file_path}")
                        transcription = transcribe_audio(audio_file_path)
                        # Save transcription to the 'transcripts' folder
                        save_transcription_to_docx(transcription, file)
                        found_audio_file = True
                        break  # Exit the inner loop if file is found
                if found_audio_file:
                    break  # Exit the outer loop if file is found
            if not found_audio_file:
                time.sleep(5)  # Wait for 30 seconds before checking again
        
        if not found_audio_file:
            print("No audio file found in the new folder within the timeout period.")
def transcribe_audio(audio_file_path):
    try:
        with open(audio_file_path, 'rb') as audio_file:
            response = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )
        return response.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""

def save_transcription_to_docx(transcription, audio_filename):
    # Ensure the 'transcripts' folder exists
    transcripts_folder = os.path.join(os.getcwd(), "transcripts")
    os.makedirs(transcripts_folder, exist_ok=True)
    
    print(transcription)
    docx_filename = audio_filename.replace('.m4a', '.txt')  # Assuming audio_filename has .mp3 extension
    docx_path = os.path.join(transcripts_folder, docx_filename)
    print(docx_path)
    with open(docx_path, 'a', encoding='utf-8') as file:
        file.write(transcription)
    print(f"Transcription saved to {docx_path}")
    main(docx_path)

if __name__ == "__main__":
    path = "C:\\Users\\shrey\\Documents\\zoom"
    event_handler = NewFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"Monitoring {path} for new folders...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
