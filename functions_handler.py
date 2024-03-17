# functions_handler.py

import requests

class FunctionsHandler:
    def __init__(self, assistant_manager):
        self.assistant_manager = assistant_manager
        # Your specific Zapier Webhook URL
        self.zapier_webhook_url = "https://hooks.zapier.com/hooks/catch/82343/19816978ac224264aa3eec6c8c911e10/"

    def send_message_to_zapier_with_thread_id(self, message, thread_id):
        """Sends a message along with the thread ID to the Zapier webhook."""
        # Payload includes the message and thread_id to be sent to Zapier
        payload = {"message": message, "thread_id": thread_id}

        # POST request to the Zapier Webhook URL with the payload
        response = requests.post(self.zapier_webhook_url, json=payload)

        # Check if the request to Zapier was successful
        if response.ok:
            print("Message successfully sent to Zapier.")
            # Optionally, you can return True and the response text for further processing
            return True, response.text
        else:
            print(f"Failed to send message to Zapier: {response.text}")
            # Return False and the error response text
            return False, response.text

# The FunctionsHandler can be used in your main controller script like so:
# functions_handler = FunctionsHandler(assistant_manager_instance)
# success, response = functions_handler.send_message_to_zapier_with_thread_id("Hello, Zapier!", "thread_id_here")
