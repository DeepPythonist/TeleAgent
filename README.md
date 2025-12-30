# TeleAgent

A Telegram AI Userbot powered by OpenAI, built with Telethon.

## Features

- **!ask <query>**: Replaces your message with the AI's response (handles edits).
- **!help**: Shows usage instructions.
- **Deep Context**: Reply to a message, and the bot will read the entire reply chain (history + sender names + timestamps) as context.
- **Configurable Backend**: Works with OpenAI or any OpenAI-compatible API.
- **Modular Design**: Clean code structure with `config.py`, `text.py`, and `prompt.py`.

## Requirements

- Python 3.8+
- Telegram API ID and Hash
- OpenAI API Key

## Setup

1.  Clone the repository.
2.  Rename `.env.example` to `.env` and fill in your credentials.
    ```env
    API_ID=your_api_id
    API_HASH=your_api_hash
    OPENAI_API_KEY=your_openai_key
    OPENAI_API_BASE=https://api.openai.com/v1 # Optional: For custom APIs
    MODEL_NAME=gpt-3.5-turbo # Optional: Select your model
    OWNER_ID=123456789 # Optional: Strict user ID check
    ```
3.  Run the launcher:
    ```bash
    python launcher.py
    ```
    *On the first run, you will be asked to enter your phone number and login code to authenticate.*

## Structure

- `main.py`: Core bot logic.
- `launcher.py`: Helper script to setup and run the bot.
- `config.py`: Configuration management.
- `text.py`: Static strings and messages.
- `prompt.py`: AI system instructions.