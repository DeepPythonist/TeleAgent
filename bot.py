import os
from datetime import datetime
from typing import Optional, List, Callable, Awaitable

from dotenv import load_dotenv
from pyrogram import Client, filters, types
from google import genai


class Settings:

    def __init__(self):
        load_dotenv(dotenv_path='.env')
        self.api_hash: Optional[str] = os.getenv('API_HASH')
        self.api_id: Optional[str] = os.getenv('API_ID')
        self.gemini_token: Optional[str] = os.getenv('GEMINI_TOKEN')
        self.admin_id: Optional[str] = os.getenv('CLIENT_ID')
        self.session_name: Optional[str] = os.getenv('SESSION_NAME', 'telegram_bot_session')
        self.model_name: Optional[str] = os.getenv('MODEL', 'gemini-pro')
        self._validate()

    def _validate(self):
        required_vars = ['api_hash', 'api_id', 'gemini_token', 'admin_id']
        missing_vars = [var for var in required_vars if not getattr(self, var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


class GeminiService:

    def __init__(self, api_key: str, model_name: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = f"models/{model_name}"
        self.base_prompt_instruction = "شما یک دستیار هوشمند در یک چت تلگرامی هستید. پاسخ‌های شما باید به زبان فارسی، کوتاه و مفید باشد."

    def _generate_content(self, prompt: str) -> str:
        try:
            print(prompt)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating content from Gemini: {e}")
            return "متاسفانه در تولید پاسخ خطایی رخ داد."

    def generate_simple_response(self, rule: str) -> str:
        prompt = f"""
{self.base_prompt_instruction}

دستور کاربر:
---
{rule}
---
"""
        print(prompt)
        return self._generate_content(prompt)

    def generate_reply_response(self, replies_chain: str, rule: str) -> str:
        prompt = f"""
{self.base_prompt_instruction}
شما باید بر اساس تاریخچه مکالمه، به آخرین دستور پاسخ دهید.

تاریخچه مکالمه (از قدیمی‌ترین به جدیدترین):
---
{replies_chain}
---

آخرین دستور:
---
{rule}
---
"""
        print(prompt)
        return self._generate_content(prompt)


class TelegramBot:

    def __init__(self, settings: Settings, gemini_service: GeminiService):
        self.settings = settings
        self.gemini = gemini_service
        self.client = Client(
            name=self.settings.session_name,
            api_hash=self.settings.api_hash,
            api_id=int(self.settings.api_id)
        )
        self._register_handlers()

    def _register_handlers(self):
        admin_filter = filters.user(int(self.settings.admin_id))

        self.client.on_message(
            filters.reply & admin_filter & filters.regex(r'^!hey reply')
        )(self.on_replied_message)

        self.client.on_message(
            filters.text & admin_filter & filters.regex(r'^!hey(?! reply)')
        )(self.on_message)

    @staticmethod
    async def build_reply_chain(agent: Client, message: types.Message) -> str:
        messages_list: List[types.Message] = []
        current_id = message.id
        chat_id = message.chat.id

        while True:
            try:
                msg = await agent.get_messages(chat_id, current_id)
                messages_list.append(msg)
                if not msg.reply_to_message_id:
                    break
                current_id = msg.reply_to_message_id
            except Exception:
                break

        messages_list.reverse()

        lines = []
        for m in messages_list:
            user_name = getattr(m.from_user, "first_name", "ناشناس")
            timestamp = m.date.strftime("%H:%M") if isinstance(m.date, datetime) else "نامشخص"
            text = m.text or "[بدون متن]"
            lines.append(f'{user_name} | {timestamp} گفت: "{text}"')

        final_lines = lines[:-1] if lines else []
        return "\n↪️ ".join(final_lines)

    async def _process_command(self, agent: Client, message: types.Message,
                               response_generator: Callable[[], Awaitable[str]]):
        try:
            await agent.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text='دارم فکر میکنم ...'
            )
            response = await response_generator()
            await agent.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=response
            )
        except Exception as e:
            print(f"Failed to process command: {e}")

    async def on_replied_message(self, agent: Client, message: types.Message):
        rule = message.text.split('!hey reply', 1)[1].strip()

        async def generator():
            full_chain = await self.build_reply_chain(agent, message)
            return self.gemini.generate_reply_response(full_chain, rule)

        await self._process_command(agent, message, generator)

    async def on_message(self, agent: Client, message: types.Message):
        rule = message.text.split('!hey', 1)[1].strip()

        async def generator():
            return self.gemini.generate_simple_response(rule)

        await self._process_command(agent, message, generator)

    def run(self):
        print("Bot is starting...")
        self.client.run()
        print("Bot stopped.")


if __name__ == "__main__":
    try:
        app_settings = Settings()
        gemini_service = GeminiService(api_key=app_settings.gemini_token, model_name=app_settings.model_name)
        bot = TelegramBot(settings=app_settings, gemini_service=gemini_service)
        bot.run()
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

