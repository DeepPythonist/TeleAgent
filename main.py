from openai import AsyncOpenAI
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError
from config import Config
from text import Text
from prompt import Prompt

openai_client = AsyncOpenAI(
    api_key=Config.OPENAI_API_KEY,
    base_url=Config.OPENAI_API_BASE
)

client = TelegramClient(Config.SESSION_NAME, Config.API_ID, Config.API_HASH)

async def get_response(user_message, system_prompt):
    try:
        completion = await openai_client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"{Text.ERROR_PREFIX}{str(e)}")
        return Text.ERROR

async def get_reply_chain(message):
    chain = []
    current_msg = message
    my_id = (await client.get_me()).id
    while current_msg:
        sender = await current_msg.get_sender()
        name = Text.UNKNOWN_SENDER
        if sender:
            if sender.id == my_id:
                name = Text.ME_LABEL
            elif hasattr(sender, 'first_name') and sender.first_name:
                name = sender.first_name
                if hasattr(sender, 'last_name') and sender.last_name:
                    name += f" {sender.last_name}"
            elif hasattr(sender, 'title'):
                name = sender.title

        text = current_msg.text or Text.NO_TEXT
        time_str = current_msg.date.strftime("%Y-%m-%d %H:%M:%S")
        
        formatted_msg = Text.CHAIN_TEMPLATE.format(
            time=time_str,
            sender=name,
            message=text
        )
        chain.append(formatted_msg)
        
        current_msg = await current_msg.get_reply_message()
    
    return "\n".join(reversed(chain))

@client.on(events.NewMessage(outgoing=True, pattern=r'^!help$'))
async def help_handler(event):
    if Config.OWNER_ID and event.sender_id != Config.OWNER_ID:
        return
    await event.edit(Text.HELP)

@client.on(events.NewMessage(outgoing=True, pattern=r'^!ask(?:\s+(.*))?$'))
async def ask_handler(event):
    if Config.OWNER_ID and event.sender_id != Config.OWNER_ID:
        return

    query = event.pattern_match.group(1)
    
    reply_to_id = event.reply_to_msg_id
    await event.delete()
    
    if not query:
        query = Text.AUTO_QUERY
    
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg:
            full_chain_str = await get_reply_chain(reply_msg)
            full_chain = full_chain_str.split('\n')
            
            target_text = full_chain[-1]
            history_text = "\n".join(full_chain[:-1]) if len(full_chain) > 1 else "No previous history."
            
            user_message = Text.CONTEXT_TEMPLATE.format(
                history_text=history_text,
                target_text=target_text,
                user_text=query
            )
            response = await get_response(user_message, Prompt.SYSTEM)
        else:
            response = await get_response(query, Prompt.SYSTEM)
    else:
        if query == Text.AUTO_QUERY:
             return
        else:
             response = await get_response(query, Prompt.SYSTEM)
        
    if reply_to_id:
        await client.send_message(event.chat_id, response, reply_to=reply_to_id)
    else:
        await client.send_message(event.chat_id, response)

def main():
    client.start()
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
