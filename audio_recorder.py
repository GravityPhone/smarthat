import os
import sys
import pyaudio
import wave
import threading

# Context manager to suppress stderr
class SuppressStderr:
    def __enter__(self):
        self.original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stderr.close()
        sys.stderr = self.original_stderr

class AudioRecorder:
    def __init__(self, output_filename="recorded_audio.wav"):
        self.output_filename = output_filename
        self.is_recording = False
        self.frames = []
        self.thread = None
        self.pyaudio_instance = None
        self.stream = None

    def _record_audio(self):
        """Internal method to handle the audio recording."""
        # Suppress ALSA warnings during PyAudio initialization
        with SuppressStderr():
            self.pyaudio_instance = pyaudio.PyAudio()
            self.stream = self.pyaudio_instance.open(format=pyaudio.paInt16,
                                                     channels=1,
                                                     rate=16000,
                                                     input=True,
                                                     frames_per_buffer=1024)
        while self.is_recording:
            data = self.stream.read(1024, exception_on_overflow=False)
            self.frames.append(data)

        # Stop and close the stream properly
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio_instance.terminate()

        # Save the recording to a WAV file
        with wave.open(self.output_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.pyaudio_instance.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(self.frames))

    def start_recording(self):
        """Starts the audio recording."""
        if not self.is_recording:
            self.is_recording = True
            self.frames = []
            self.thread = threading.Thread(target=self._record_audio)
            self.thread.start()
            print("Recording started...")

    def stop_recording(self):
        """Stops the audio recording."""
        if self.is_recording:
            self.is_recording = False
            self.thread.join()  # Wait for the recording thread to finish
            print("Recording stopped.")

# Global instance to be used outside this script
recorder = AudioRecorder()

def start_recording():
    """Function to start recording, intended to be called from elsewhere."""
    recorder.start_recording()

def stop_recording():
    """Function to stop recording, intended to be called from elsewhere."""
    recorder.stop_recording()
