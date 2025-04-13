import os
import subprocess
from pydub import AudioSegment
from pydub.utils import which

# Ensure ffmpeg is found
AudioSegment.converter = which("ffmpeg")

def extract_audio_from_webm(input_file, output_dir, output_format="wav"):
    """
    Extracts all audio streams from a .webm file and saves them as separate files.
    
    Args:
    - input_file (str): Path to the input .webm file.
    - output_dir (str): Directory where the extracted audio files will be saved.
    - output_format (str): Output audio format (e.g., "wav", "mp3", "flac").
    
    Returns:
    - List of extracted audio file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(input_webm)
    print(output_folder)
    # Get audio stream count using ffprobe
    cmd_probe = [
        "ffprobe", "-i", input_file, "-show_streams", "-select_streams", "a", "-loglevel", "error"
    ]
    result = subprocess.run(cmd_probe, capture_output=True, text=True)
    
    # Count the number of audio streams
    stream_count = result.stdout.count("[STREAM]")
    
    if stream_count == 0:
        print("No audio streams found in the file.")
        return []
    
    extracted_files = []

    for i in range(stream_count):
        output_file = os.path.join(output_dir, f"audio_track_{i+1}.{output_format}")
        
        cmd_extract = [
            "ffmpeg", "-i", input_file,
            "-map", f"0:a:{i}",  # Extract the specific audio stream
            "-acodec", "pcm_s16le" if output_format == "wav" else "libmp3lame",
            output_file, "-y"
        ]
        
        subprocess.run(cmd_extract, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(output_file):
            extracted_files.append(output_file)
            print(f"Extracted: {output_file}")

    return extracted_files

# Example usage
input_webm = "G:/project/sample-9.webm"  # Ensure this file exists
output_folder = "G:/project/extracted_audio/"
print(input_webm)
print(output_folder)
extracted_files = extract_audio_from_webm(input_webm, output_folder, "wav")

if extracted_files:
    print("Extraction complete! Extracted audio files:", extracted_files)
else:
    print("No audio files were extracted.")