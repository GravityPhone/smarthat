import subprocess
import os
import base64
import uuid
import threading
import requests

class VisionModule:
    def __init__(self, openai_api_key):
        self.api_key = openai_api_key
        self.capture_complete = threading.Event()

    def capture_image_async(self):
        """Initiates the image capture process in a new thread."""
        self.capture_complete.clear()  # Reset the event for the new capture process
        thread = threading.Thread(target=self.capture_image)
        thread.start()

    def capture_image(self):
        """Captures an image using fswebcam and saves it as a PNG file."""
        image_file_name = f"{uuid.uuid4()}.png"
        self.image_path = f"/tmp/{image_file_name}"
        print("Taking picture now...")
        capture_command = f"fswebcam --no-banner --resolution 1280x720 --save {self.image_path} -d /dev/video0 -r 1280x720 --png 1"

        try:
            subprocess.check_call(capture_command.split())
            print(f"Image captured successfully: {self.image_path}")
            self.capture_complete.set()  # Signal that the capture has completed
        except subprocess.CalledProcessError as e:
            print(f"Failed to capture image: {e}")
            self.image_path = None  # Ensure path is reset on failure
            self.capture_complete.set()  # Signal to unblock any waiting process, even though capture failed

    def encode_image_to_base64(self):
        """Encodes the captured image to a base64 string."""
        if self.image_path and os.path.exists(self.image_path):
            with open(self.image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        else:
            print("No image file found or image capture failed.")
        return None

    def get_image_description(self, transcription, base64_image):
        """Sends the base64-encoded image along with the transcription to the OpenAI API and returns the description."""
        if base64_image:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": transcription},  # Use transcription as the prompt
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                        ]
                    }
                ],
                "max_tokens": 300
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            if response.status_code == 200:
                try:
                    return response.json()['choices'][0]['message']['content']
                except KeyError:
                    return "Description not available or wrong response format."
            else:
                print(f"Error in OpenAI API call: {response.text}")
        return "Failed to encode image or image capture failed."

    def describe_captured_image(self, transcription="What's in this image?"):
        """Ensures the image capture has completed, then encodes and sends it along with the transcription to the OpenAI API for a description."""
        self.capture_complete.wait()  # Wait for the image capture to complete
        base64_image = self.encode_image_to_base64()
        if base64_image:
            description = self.get_image_description(transcription, base64_image)
            print(f"Sending image description request...")
            # Cleanup
            if self.image_path and os.path.exists(self.image_path):
                os.remove(self.image_path)
            return description
        else:
            return "Image processing failed."
