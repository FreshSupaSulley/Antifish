import discord
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load env variables
load_dotenv()

intents = discord.Intents.default()
# Docs say to turn this on
intents.reactions = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# I am allowed to fish react
OWNER_ID = os.environ.get('OWNER_ID');

@client.event
async def on_raw_reaction_add(event):
    print(f"RAW REACTION {event.emoji}")
    # I am allowed to fish react (tyranny)
    if event.member.bot or event.user_id is OWNER_ID:
        return
    if event.emoji.name == "🐟":
        print(f"Detected fish reaction from {event.member.name}")
        # Delete the message
        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=on_reaction#discord.WebhookMessage.remove_reaction
        try:
            channel = client.get_channel(event.channel_id)
            message = await channel.fetch_message(event.message_id)
            await message.remove_reaction(event.emoji, event.member)
            print(f"Deleted message ID {event.message_id} after fish reaction")
            # Now timeout the member
            await event.member.timeout(timedelta(minutes=1), reason="Fish reactions are banned")
        except Exception as e:
            print(f"Failed to delete reaction: {e}")

# Start
client.run(os.environ.get('BOT_TOKEN'))
