# Signal Chatbot

This is a friendly AI chatbot designed to interact with users over Signal. It utilizes the Ollama language model to generate responses. 

## Features

- Friendly and engaging chatbot
- First-person perspective responses
- Supports continuous conversation history
- Integrates with Signal for message sending and receiving

## Dependencies

- Python 3.8+
- `signal-cli` (Signal Command Line Interface)
- `ollama` Python package
- `dotenv` Python package

`pip3 install python-dotenv ollama`

## Setup Virtual Environment

`python3 -m venv venv`

`source venv/bin/activate`

## Make A .env File

`PHONE_NUMBER_BOT=your_signal_phone_number`

`PHONE_NUMBER_TARGET=target_signal_phone_number`

`BOT_NAME=YourBotName`

`USER_NAME=YourUserName`

## Requirements

- A decently powerful computer or a server with an RTX series GPU
- A system running Linux or at least WSL with Linux installed

For more details on the hardware requirements for running Ollama models, please refer to this [resource](https://quickcreator.io/quthor_blog/essential-ollama-hardware-requirements-for-top-performance/#:~:text=To%20embark%20on%20your%20Ollama,handle%20the%20computational%20demands%20effectively).

## Models

Models can be found in the [Ollama library](https://ollama.com/library). You can download models using the following command:

```bash
ollama pull [REPLACE_WITH_MODEL]
