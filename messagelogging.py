import discord
import aiohttp
import random

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

WEBHOOK_URL = 'https://discord.com/api/webhooks/1134502151578734782/35kEwlFJ8Lvda9810Re3ZUT6tDk0Sy5Q05GO47AqBetxA8RatIblCxDiSfJPwYIG-Dzb'

excluded_channel_ids = [
    997900675621081228
]
excluded_category_id = 872030224127246346


def is_channel_excluded(channel):
    return channel.id in excluded_channel_ids or (
        channel.category and channel.category.id == excluded_category_id)


def get_random_color():
    return discord.Color(random.randint(0, 0xFFFFFF))


async def send_webhook_embed(embed, username, avatar_url):
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json={"embeds": [embed.to_dict()], "username": username, "avatar_url": avatar_url}):
            pass


@bot.event
async def on_ready():
    print(f"Message Logging")


@bot.event
async def on_message_edit(before, after):
    if not is_channel_excluded(before.channel):
        if not before.author.bot and before.author.id != bot.user.id:
            message_link = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
            embed = discord.Embed(
                title=f"Message edited in #{before.channel.name}",
                description=f"Message Link: [Click here]({message_link})",
                color=get_random_color())
            embed.add_field(name="Author", value=before.author.display_name, inline=False)
            embed.add_field(name="Before", value=before.content, inline=False)
            if after.content:
                embed.add_field(name="After", value=after.content, inline=False)
            else:
                embed.add_field(name="After", value="(Message deleted)", inline=False)

            # Check if an image is attached
            if after.attachments:
                image_url = after.attachments[0].url
                embed.set_image(url=image_url)  # Set the image URL

            await send_webhook_embed(embed, before.author.display_name, before.author.avatar.url if before.author.avatar else None)


@bot.event
async def on_message_delete(message):
    if not is_channel_excluded(message.channel):
        if not message.author.bot and message.author.id != bot.user.id:
            message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
            embed = discord.Embed(
                title=f"Message deleted in #{message.channel.name}",
                description=f"Message Link: [Click here]({message_link})",
                color=get_random_color())
            embed.add_field(name="Author", value=message.author.display_name, inline=False)
            embed.add_field(
                name="Message",
                value=message.content if message.content else "(No Text)",
                inline=False)

            # Check if an image is attached
            if message.attachments:
                image_url = message.attachments[0].url
                embed.set_image(url=image_url)  # Set the image URL

            await send_webhook_embed(embed, message.author.display_name, message.author.avatar.url if message.author.avatar else None)

bot.run("TOKEN")
