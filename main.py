import json
import logging
from tqdm import tqdm
from telethon import TelegramClient, events
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

@client.on(events.NewMessage)
async def handler(event):
    try:
        chat = await event.get_chat()
        chat_id = chat.id
        chat_name = await get_entity_name(chat)

        # Logging pour débogage
        logging.debug(f"Received message from chat_id: {chat_id}, chat_name: {chat_name}")
        
        # Vérifier si le message provient d'un des canaux ou groupes sources
        if chat_name in source_channels or str(chat_id) in source_channels:
            # Récupérer le canal ou groupe cible
            target_channel_entity = await client.get_entity(target_channel)
            target_name = await get_entity_name(target_channel_entity)
            
            # Vérifier le type de média et le reposter dans le canal cible
            if event.message.media:
                if isinstance(event.message.media, MessageMediaPhoto):
                    await client.send_file(target_channel_entity, event.message.media.photo, caption=event.message.message)
                    logging.info(f"Photo reposted from {chat_name} to {target_name}")
                elif isinstance(event.message.media, MessageMediaDocument):
                    await client.send_file(target_channel_entity, event.message.media.document, caption=event.message.message)
                    logging.info(f"Document reposted from {chat_name} to {target_name}")
            else:
                # Reposter le message texte dans le canal cible
                await client.send_message(target_channel_entity, event.message.message)
                logging.info(f"Message reposted from {chat_name} to {target_name}")

            # Print pour la visibilité immédiate
            print(f"Message from {chat_name} reposted to {target_name}")

    except Exception as e:
        logging.error(f"Error handling message from chat_id: {chat_id}: {e}")
        print(f"Error handling message from chat_id: {chat_id}: {e}")

async def main():
    await client.start(phone_number)
    print("Bot is running...")
    logging.info("Bot started")

    # Utiliser tqdm pour afficher une barre de progression
    with tqdm(total=0, desc="Processing messages", unit="msg") as pbar:
        @client.on(events.NewMessage)
        async def handler(event):
            try:
                chat = await event.get_chat()
                chat_id = chat.id
                chat_name = await get_entity_name(chat)

                # Logging pour débogage
                logging.debug(f"Received message from chat_id: {chat_id}, chat_name: {chat_name}")
                
                # Vérifier si le message provient d'un des canaux ou groupes sources
                if chat_name in source_channels or str(chat_id) in source_channels:
                    # Récupérer le canal ou groupe cible
                    target_channel_entity = await client.get_entity(target_channel)
                    target_name = await get_entity_name(target_channel_entity)

                    # Vérifier le type de média et le reposter dans le canal cible
                    if event.message.media:
                        if isinstance(event.message.media, MessageMediaPhoto):
                            await client.send_file(target_channel_entity, event.message.media.photo, caption=event.message.message)
                            logging.info(f"Photo reposted from {chat_name} to {target_name}")
                        elif isinstance(event.message.media, MessageMediaDocument):
                            await client.send_file(target_channel_entity, event.message.media.document, caption=event.message.message)
                            logging.info(f"Document reposted from {chat_name} to {target_name}")
                    else:
                        # Reposter le message texte dans le canal cible
                        await client.send_message(target_channel_entity, event.message.message)
                        logging.info(f"Message reposted from {chat_name} to {target_name}")

                    # Print pour la visibilité immédiate
                    print(f"Message from {chat_name} reposted to {target_name}")

                    # Incrémenter la barre de progression
                    pbar.update(1)

            except Exception as e:
                logging.error(f"Error handling message from chat_id: {chat_id}: {e}")
                print(f"Error handling message from chat_id: {chat_id}: {e}")

    # Garde le script en cours d'exécution
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
