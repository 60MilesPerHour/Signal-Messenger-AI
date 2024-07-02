import subprocess
import time
import re
import os
import asyncio
from dotenv import load_dotenv
import ollama

# Load environment variables from .env file
load_dotenv()
PHONE_NUMBER = os.getenv('PHONE_NUMBER_BOT')
TARGET_NUMBER = os.getenv('PHONE_NUMBER_TARGET')

# Store the history of interactions
history = {}
response_task = {}
music_preferences = {}

# Placeholder values, which can be customized
BOT_NAME = os.getenv('BOT_NAME')
USER_NAME = os.getenv('USER_NAME')

initial_context = {
    "role": "system",
    "content": (
        f"You are {BOT_NAME}, a friendly AI who loves to chat with {USER_NAME}. "
        "In your responses, always use 'my' in reference to yourself and say {USER_NAME} when addressing them. The idea here is to be in first-person perspective at all times."
    )
}

async def send_message(to, message):
    try:
        subprocess.run(["/usr/local/bin/signal-cli", "-u", PHONE_NUMBER, "send", "-m", message, to], check=True)
        print(f"Sent message '{message}' to {to}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to send message: {e}")

async def receive_messages():
    try:
        result = subprocess.run(["/usr/local/bin/signal-cli", "-u", PHONE_NUMBER, "receive"], capture_output=True, text=True, check=True)
        messages = result.stdout.strip()
        if not messages:
            print("No new messages received.")
            return []
        
        return messages.split("\n\n")  # Split messages by double newline
    except subprocess.CalledProcessError as e:
        print(f"Failed to receive messages: {e}")
        return []

def parse_message(raw_message):
    # Regular expression to extract relevant parts of the message
    envelope_match = re.search(r'Envelope from: .+ (\+\d+) \(device: \d+\) to .+', raw_message)
    body_match = re.search(r'Body: (.+)', raw_message)
    
    if envelope_match and body_match:
        sender = envelope_match.group(1)
        body = body_match.group(1)
        return sender, body
    return None, None

async def handle_music_preference(sender, content):
    global music_preferences

    # Extract album or song name
    if 'album' in content:
        keyword = 'album'
    elif 'song' in content:
        keyword = 'song'
    else:
        return

    music_item = content.split(keyword)[-1].strip()
    if sender not in music_preferences:
        music_preferences[sender] = {}

    if music_item not in music_preferences[sender]:
        music_preferences[sender][music_item] = False
        await send_message(sender, f"I haven't listened to {music_item} yet, but I'll give it a try and let you know what I think!")
    else:
        await send_message(sender, f"I've listened to {music_item}. Here's what I think: It's fantastic! The melodies and lyrics are captivating.")

# Get response from Ollama for regular chat
async def get_ollama_response(sender, prompt):
    global history
    if sender not in history:
        history[sender] = [initial_context]
    context = history[sender]
    context.append({"role": "user", "content": prompt})
    
    response = ollama.chat(model='llama3', messages=context)
    
    response_text = response['message']['content']
    context.append({"role": "assistant", "content": response_text})
    history[sender] = context[-20:]  # Keep the last 20 messages

    return response_text

async def main():
    print("Starting Signal bot...")
    while True:
        print("Checking for new messages...")
        messages = await receive_messages()
        if not messages:
            print("No messages to process.")
        for raw_message in messages:
            print(f"Received raw message: {raw_message}")
            sender, body = parse_message(raw_message)
            if sender and body:
                print(f"Message from {sender}: {body}")

                # Check for music preferences
                if 'album' in body.lower() or 'song' in body.lower():
                    await handle_music_preference(sender, body)
                    continue

                try:
                    response = await get_ollama_response(sender, body)
                    await send_message(sender, response)
                except Exception as e:
                    await send_message(sender, f"An error occurred: {str(e)}")
        await asyncio.sleep(1)  # Check for new messages every 1 second

if __name__ == "__main__":
    asyncio.run(main())
