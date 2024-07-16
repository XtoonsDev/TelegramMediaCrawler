import json
import logging
import asyncio
from tqdm import tqdm
from telethon import TelegramClient, events, errors
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Configurer le logging
logging.basicConfig(
    filename='telegram_crawler.log',
    level=logging.DEBUG,  # Passer à DEBUG pour plus de détails
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Charger la configuration et le mapping des canaux
with open('config/config.json', 'r') as f:
    config = json.load(f)

with open('config/channels.json', 'r') as f:
    source_channels = json.load(f)

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
                logging.info(f"Photo repostée de {chat_name} vers {target_name}")
            elif isinstance(event.message.media, MessageMediaDocument):
                await client.send_file(target_channel_entity, event.message.media.document, caption=event.message.message)
                logging.info(f"Document reposté de {chat_name} vers {target_name}")
        else:
            await client.send_message(target_channel_entity, event.message.message)
            logging.info(f"Message reposté de {chat_name} vers {target_name}")

        print(f"Message de {chat_name} reposté vers {target_name}")
    except errors.FloodWaitError as e:
        logging.warning(f"Erreur de limite de requêtes: attente de {e.seconds} secondes")
        await asyncio.sleep(e.seconds)
        await repost_message(event, target_channel_entity, chat_name, target_name)
    except Exception as e:
        logging.error(f"Erreur lors du repostage du message de {chat_name} vers {target_name}: {e}")
        print(f"Erreur lors du repostage du message de {chat_name} vers {target_name}: {e}")

@client.on(events.NewMessage)
async def handler(event):
    try:
        chat = await event.get_chat()
        chat_id = chat.id
        chat_name = await get_entity_name(chat)

        logging.debug(f"Message reçu de chat_id: {chat_id}, chat_name: {chat_name}")
        
        if chat_name in source_channels or str(chat_id) in source_channels:
            target_channel_entity = await client.get_entity(target_channel)
            target_name = await get_entity_name(target_channel_entity)
            await repost_message(event, target_channel_entity, chat_name, target_name)

            with tqdm(total=1, desc="Traitement des messages", unit="msg") as pbar:
                pbar.update(1)
    except Exception as e:
        logging.error(f"Erreur lors du traitement du message de chat_id: {chat_id}: {e}")
        print(f"Erreur lors du traitement du message de chat_id: {chat_id}: {e}")

async def main():
    await client.start(phone_number)
    print("Le bot fonctionne...")
    logging.info("Bot démarré")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
