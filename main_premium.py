import json
import logging
import asyncio
from tqdm import tqdm
from telethon import TelegramClient, events, errors
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Charger la configuration
with open('config/config.json', 'r') as f:
    config = json.load(f)

# Charger les traductions depuis le dossier "lang"
language = config.get('language', 'en')
with open(f'lang/translations_{language}.json', 'r') as f:
    translations = json.load(f)

def translate(key, **kwargs):
    return translations[key].format(**kwargs)

# Configurer le logging
logging.basicConfig(
    filename='telegram_crawler.log',
    level=logging.DEBUG,  # Passer à DEBUG pour plus de détails
    format='%(asctime)s - %(levelname)s - %(message)s'
)

api_id = config['api_id']
api_hash = config['api_hash']
phone_number = config['phone_number']
target_channel = config['target_channel']

client = TelegramClient('session_name', api_id, api_hash)

async def get_entity_name(entity):
    """Helper function to get entity name for logging."""
    return entity.username if hasattr(entity, 'username') else str(entity.id)

async def repost_message(event, target_channel_entity, chat_name, target_name):
    try:
        if event.message.media:
            if isinstance(event.message.media, MessageMediaPhoto):
                await client.send_file(target_channel_entity, event.message.media.photo, caption=event.message.message)
                logging.info(translate("photo_reposted", chat_name=chat_name, target_name=target_name))
            elif isinstance(event.message.media, MessageMediaDocument):
                await client.send_file(target_channel_entity, event.message.media.document, caption=event.message.message)
                logging.info(translate("document_reposted", chat_name=chat_name, target_name=target_name))
        else:
            await client.send_message(target_channel_entity, event.message.message)
            logging.info(translate("message_reposted", chat_name=chat_name, target_name=target_name))

        print(translate("message_reposted", chat_name=chat_name, target_name=target_name))
    except errors.FloodWaitError as e:
        logging.warning(translate("flood_wait_error", seconds=e.seconds))
        await asyncio.sleep(e.seconds)
        await repost_message(event, target_channel_entity, chat_name, target_name)
    except Exception as e:
        logging.error(translate("error_handling_message", chat_id=chat.id, error=str(e)))
        print(translate("error_handling_message", chat_id=chat.id, error=str(e)))

@client.on(events.NewMessage)
async def handler(event):
    try:
        chat = await event.get_chat()
        chat_id = chat.id
        chat_name = await get_entity_name(chat)

        logging.debug(f"Received message from chat_id: {chat_id}, chat_name: {chat_name}")
        
        if chat_name in source_channels or str(chat_id) in source_channels:
            target_channel_entity = await client.get_entity(target_channel)
            target_name = await get_entity_name(target_channel_entity)
            await repost_message(event, target_channel_entity, chat_name, target_name)

            with tqdm(total=1, desc="Processing messages", unit="msg") as pbar:
                pbar.update(1)
    except Exception as e:
        logging.error(translate("error_handling_message", chat_id=chat_id, error=str(e)))
        print(translate("error_handling_message", chat_id=chat_id, error=str(e)))

async def main():
    await client.start(phone_number)
    print(translate("bot_started"))
    logging.info(translate("bot_started"))
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
