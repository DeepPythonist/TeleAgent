class Text:
    HELP = """
**TeleAgent Help**

Use the following commands:
- `!ask <question>`: Ask the AI a question. The bot will edit your message with the answer.
- `!help`: Show this help message.
"""
    PROCESSING = "Thinking..."
    ERROR = "An error occurred. Please try again later."
    ERROR_PREFIX = "Error: "
    CONTEXT_TEMPLATE = "Conversation History:\n{history_text}\n\nTarget Message (Reply to this):\n{target_text}\n\nUser Instruction/Draft: {user_text}"
    CHAIN_TEMPLATE = "[{time}] {sender}: {message}"
    NO_TEXT = "[Media/No Text]"
    UNKNOWN_SENDER = "Unknown"
    ME_LABEL = "Me (Marcel)"
    AUTO_QUERY = "Analyze the conversation above and provide a relevant, natural response as Me (Marcel)."
    ASK_USAGE_ERROR = "Please provide a question or reply to a message to use !ask."
