import os
from elevenlabs import generate, play, set_api_key, Voice

class ElevenLabsManager:
    def __init__(self, api_key):
        """
        Initializes the ElevenLabsManager with the given API key.
        """
        self.api_key = api_key
        # Removed the call to configure_api_key since we'll pass the API key directly

    def play_text(self, text, voice_id="RXZFrCz94YM9cSj7aieu", model="eleven_turbo_v2"):
        """
        Generates audio from text using the specified voice and model, then plays the audio.
        The function explicitly passes the API key to the generate function.
        """
        try:
            voice = Voice(voice_id=voice_id)  # Create a Voice object with the custom voice ID
            audio = generate(
                text=text,
                voice=voice,
                model=model,
                api_key=self.api_key  # Pass the API key directly
            )
            if audio:
                play(audio)
            else:
                print("Failed to generate audio.")
        except Exception as e:
            print(f"Error generating or playing audio: {e}")

# Example usage:
if __name__ == "__main__":
    eleven_labs_api_key = "1ffd6c1025c9a8c485e5b779feedef6a"  # Replace with your actual Eleven Labs API key
    eleven_labs_manager = ElevenLabsManager(eleven_labs_api_key)
    eleven_labs_manager.play_text("Hello! This is a test of the Eleven Labs TTS API.")
