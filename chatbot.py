import os
import pygame
from google.cloud import texttospeech
import logging

logging.basicConfig(level=logging.INFO)

# Check if Google Cloud credentials file exists
if not os.path.exists("API.json"):
    raise FileNotFoundError("Google Cloud credentials file not found.")

# Set your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "API.json"

# Initialize the Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

def speak(text, filename="response.mp3"):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(filename, "wb") as out:
        out.write(response.audio_content)

    play_audio(filename)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(filename)

def play_audio(file_path):
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(f"Error initializing pygame mixer: {e}")
        return

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def chatbot_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hey there! How can I assist you today?"
    elif "how are you" in user_input:
        return "I'm great! Ready to chat with you."
    elif "bye" in user_input:
        return "Goodbye! See you next time."
    else:
        return "Hmm, I'm not sure how to respond to that yet."

# Chatbot Loop
logging.info("Chatbot started.")
print("Chatbot is running. Type 'bye' to quit.\n")
while True:
    user_input = input("You: ")
    response = chatbot_response(user_input)
    print("Bot:", response)
    try:
        speak(response)
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
    if "bye" in user_input.lower():
        break