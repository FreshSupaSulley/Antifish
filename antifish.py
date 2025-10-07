import discord
import os
from dotenv import load_dotenv
from datetime import timedelta
import emoji

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
illegal_reactions = ["shrimp", "fish", "octopus", "tropical_fish", "fish_cake", "fishing_pole_and_fish", "fishing_pole", "blowfish", "jellyfish", "shark", "lobster", "crab", "squid", "whale", "whale2", "oyster", "fried_shrimp", "seal", "dolphin", "coral", "crocodile", "seaweed"]

@client.event
async def on_raw_reaction_add(event):
    emoji_name = emoji.demojize(event.emoji.name).strip(":")
    print(f"Reaction added: {event.emoji} ({emoji_name}) by {event.member}")
    if emoji_name in illegal_reactions:
        print(f"Detected fish reaction from {event.member.name}: {event.emoji}")
        # I am allowed to fish react (tyranny)
        if event.member.bot or str(event.user_id) == str(OWNER_ID):
            print("Priviledge user, fish reaction will slide")
            return
        # Delete the message
        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=on_reaction#discord.WebhookMessage.remove_reaction
        try:
            channel = client.get_channel(event.channel_id)
            message = await channel.fetch_message(event.message_id)
            await message.remove_reaction(event.emoji, event.member)
            print(f"USER: {event.member}")
            # Now timeout the member
            await event.member.timeout(timedelta(seconds=5), reason="Fish reactions are banned")
        except Exception as e:
            print(f"Failed to delete reaction: {e}")

# Start
client.run(os.environ.get('BOT_TOKEN'))
