import pyaudio
import wave

class SoundEffectsPlayer:
    def __init__(self):
        """Initializes the sound effects player."""
        self.pyaudio_instance = pyaudio.PyAudio()

    def play_sound(self, file_path):
        """
        Play a sound effect from the specified file path.

        Args:
        file_path (str): The path to the wave file to play.
        """
        # Open the wave file
        wf = wave.open(file_path, 'rb')

        # Open a stream for audio playback
        stream = self.pyaudio_instance.open(format=self.pyaudio_instance.get_format_from_width(wf.getsampwidth()),
                                            channels=wf.getnchannels(),
                                            rate=wf.getframerate(),
                                            output=True)

        # Read data in chunks and play
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)

        # Cleanup
        stream.stop_stream()
        stream.close()

    def __del__(self):
        """Ensure PyAudio instance is terminated upon deletion."""
        self.pyaudio_instance.terminate()
