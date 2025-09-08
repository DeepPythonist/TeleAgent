import os
from typing import Optional

from google import genai
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message


class Settings:
    def __init__(self):
        load_dotenv()
        self.api_hash: str = self._get_env("API_HASH")
        self.api_id: int = int(self._get_env("API_ID"))
        self.gemini_token: str = self._get_env("GEMINI_TOKEN")
        self.admin_id: int = int(self._get_env("CLIENT_ID"))
        self.session_name: str = self._get_env("SESSION_NAME")
        self.model_name: str = self._get_env("MODEL")

    @staticmethod
    def _get_env(name: str) -> str:
        value = os.getenv(name)
        if value is None:
            raise ValueError(f"Environment variable {name} is not set.")
        return value


class GeminiService:
    BASE_PROMPT = "پاسخت باید کوتاه و مفید باشه"

    def __init__(self, api_key: str, model_name: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate_content(self, rule: str, context: Optional[str] = None) -> str:
        prompt_parts = [self.BASE_PROMPT, rule]
        if context:
            prompt_parts.insert(1, context)

        full_prompt = "\n\n".join(prompt_parts)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=full_prompt,
        )
        return response.text


class TelegramBot:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.gemini = GeminiService(
            api_key=self.settings.gemini_token,
            model_name=self.settings.model_name
        )
        self.client = Client(
            name=self.settings.session_name,
            api_hash=self.settings.api_hash,
            api_id=self.settings.api_id,
        )
        self._register_handlers()

    def run(self):
        self.client.run()

    def _register_handlers(self):
        admin_filter = filters.user(self.settings.admin_id)

        self.client.on_message(
            admin_filter & filters.reply & filters.regex(r"^!hey reply")
        )(self.on_replied_message)

        self.client.on_message(
            admin_filter & filters.text & filters.regex(r"^!hey(?! reply)")
        )(self.on_standard_message)

    async def _process_command(self, message: Message, rule: str, context: Optional[str] = None):
        try:
            await message.edit_text("دارم فکر میکنم ...")
            response = self.gemini.generate_content(rule, context)
            await message.edit_text(response)
        except Exception as e:
            await message.edit_text(f"خطایی رخ داد: {e}")

    @staticmethod
    async def _build_reply_chain(message: Message) -> str:
        chain = []
        current_message = message
        while current_message.reply_to_message:
            current_message = current_message.reply_to_message
            chain.append(current_message)

        chain.reverse()

        formatted_lines = []
        for msg in chain:
            user = msg.from_user
            name = user.first_name if user else "ناشناس"
            timestamp = msg.date.strftime("%H:%M") if msg.date else "نامشخص"
            text = msg.text or "[بدون متن]"
            formatted_lines.append(f'{name} | {timestamp} گفت: "{text}"')

        return "\n↪️ ".join(formatted_lines)

    async def on_replied_message(self, _: Client, message: Message):
        rule = message.text[len("!hey reply"):].strip()
        if not rule:
            await message.edit_text("لطفاً یک دستور بعد از `!hey reply` بنویس.")
            return

        context = await self._build_reply_chain(message)
        await self._process_command(message, rule, context)

    async def on_standard_message(self, _: Client, message: Message):
        rule = message.text[len("!hey"):].strip()
        if not rule:
            await message.edit_text("لطفاً یک دستور بعد از `!hey` بنویس.")
            return
        await self._process_command(message, rule)


if __name__ == "__main__":
    app_settings = Settings()
    bot = TelegramBot(settings=app_settings)
    bot.run()

