import json
from telethon import TelegramClient

# Charger la configuration
with open('config/config.json', 'r') as f:
    config = json.load(f)

api_id = config['api_id']
api_hash = config['api_hash']
phone_number = config['phone_number']

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone_number)
    me = await client.get_me()
    print(f"Bot owner username: {me.username}")
    print(f"Bot owner ID: {me.id}")

with client:
    client.loop.run_until_complete(main())
