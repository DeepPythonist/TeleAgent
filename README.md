# 🤖 TeleAgent

> **Your intelligent, human-like Telegram Userbot powered by LLMs.**  
> *Seamlessly integrated, context-aware, and strictly secure.*

**TeleAgent** is a powerful Userbot that connects your Telegram account to OpenAI (or compatible APIs). It acts on your behalf, allowing you to reply to messages using AI with deep context awareness, while maintaining your personal style and privacy.

---

## ✨ Features

- **🧠 Deep Context Awareness**: Replies are not isolated! The bot reads the **entire reply chain** (history, sender names, timestamps) to understand the full conversation context.
- **🗣️ Human Mode**: responses are formatted like a real human (no formal punctuation, casual tone).
- **🎭 Custom Persona**: Acts as **Marcel** (or your custom identity) — a nationalist, programmer, and critical thinker.
- **👻 Ghost Mode**:
    - **Auto-Delete**: The `!ask` command is instantly deleted.
    - **Direct Reply**: The AI response is sent as a new message from *you*.
- **⚡ Smart Input**:
    - Give instructions: `!ask Roast him` -> The AI roasts the target.
    - Draft replies: `!ask I disagree` -> The AI writes a full argument based on your stance.
    - **Auto-Participate**: Reply with just `!ask` (no text) to let the AI join the conversation naturally.
- **🔒 Secure & Private**:
    - **Strict ID Check**: Only responds to commands from the `OWNER_ID`.
    - **Error Privacy**: Errors are logged to the terminal, not the chat.

---

## 🚀 Quick Start in 3 Steps

### 1. Requirements
- Python 3.8+
- A Telegram Account (Phone number)
- API Keys (Telegram & OpenAI)

### 2. Installation
Clone the repo and enter the directory:
```bash
git clone https://github.com/DeepPythonist/TeleAgent.git
cd TeleAgent
```

Create your configuration file:
1.  Rename `.env.example` to `.env`.
2.  Open `.env` and fill in your details:
    ```ini
    API_ID=123456
    API_HASH=abcdef123456...
    
    OPENAI_API_KEY=sk-proj-...
    OPENAI_API_BASE=https://api.openai.com/v1  # (Optional) Custom API URL
    MODEL_NAME=gpt-4o  # (Optional) Model name
    
    SESSION_NAME=teleagent  # (Optional) Telethon session name
    OWNER_ID=123456789  # (Optional) Restrict commands to your ID
    ```

### 3. Run!
We provided a magic launcher that handles everything (Virtual Environment, Dependencies, Updates):

```bash
python launcher.py
```

*On the first run, you will be asked to log in with your Telegram phone number.*

---

## 🎮 Usage

| Command | Description |
| :--- | :--- |
| **`!ask`** | (Reply to a message) The AI reads the history and writes a natural reply for you. |
| **`!ask <text>`** | (Reply to a message) The AI uses your text as an instruction or draft to write the reply. |
| **`!help`** | Shows the help menu in saved messages. |

---

## ⚙️ Configuration (.env)

| Variable | Description |
| :--- | :--- |
| `API_ID` / `API_HASH` | Get these from [my.telegram.org](https://my.telegram.org). |
| `OPENAI_API_KEY` | Your API key from OpenAI or a compatible provider. |
| `OPENAI_API_BASE` | (Optional) URL for custom API providers (e.g., AvalAI). |
| `MODEL_NAME` | (Optional) Model to use (e.g., `gpt-4o`, `gpt-3.5-turbo`). |
| `SESSION_NAME` | (Optional) Name of the session file (default: `teleagent_session`). |
| `OWNER_ID` | (Optional) Restrict commands to this specific User ID. |

---

<p align="center">
Made with ❤️ by <b>DeepPythonist</b>
</p>