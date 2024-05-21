import discord

intents = discord.Intents.all()

bot = discord.Client(intents=intents)

# Constants
IGNORE_CATEGORY_IDS = [1123881823496318977, 864827024405299211, 1124718600268296312, 1124717508147027989, 1117625388496076871, 1096829264113979453, 884284278446374992, 864829683693518858, 901470846961451028, 866903973331075082, 872030224127246346, 1131111784145768448, 1222841709012979834, 1222832506160807997, 1222831714099793920, 1222830432891047984, 1222833561883770900, 1222833479058722858, 1222833691844284428, 1222833791072993300, 1222833888460804157, 1228213790890393611]  # Add the category IDs to ignore here
IGNORE_CHANNEL_IDS = [1109687322108252190, 1109687898065870868, 1109688330708320266]
LOG_CHANNEL_ID = 1222102503689027675
MORE_CHANNEL_IDS = [924257183678468097, 901708635997077514, 1133309998336847882]
TRIGGER_CHANNEL_ID = 1222112797131804712
CHECK_CHANNEL_ID = 1222047102536781905
SERVER_1_ID = 864766766932426772
SERVER_2_ID = 1123881823496318976

# Function to send message to log channel
async def send_to_log_channel(message):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(message)
    else:
        print("Log channel not found.")

# Event for bot being ready
@bot.event
async def on_ready():
    print(f'Error Notify')

# Event for new messages in trigger channel
@bot.event
async def on_message(message):
    if message.channel.id == TRIGGER_CHANNEL_ID:
        last_log_message = await get_last_log_message()
        if last_log_message and last_log_message.content.lower() == 'up':
            last_check_message = await get_last_check_message()
            if last_check_message:
                time_difference = (message.created_at - last_check_message.created_at).total_seconds()
                if time_difference > 180:
                    await down() # Modification here
    if message.channel.id == CHECK_CHANNEL_ID:
        last_log_message = await get_last_log_message()
        if last_log_message and last_log_message.content.lower() == 'down':
            await up()

# Function to get the last log message
async def get_last_log_message():
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        async for message in log_channel.history(limit=1):
            return message
    else:
        print("Log channel not found.")
        return None

# Function to get the last check message
async def get_last_check_message():
    check_channel = bot.get_channel(CHECK_CHANNEL_ID)
    if check_channel:
        async for message in check_channel.history(limit=1):
            return message
    else:
        print("Check channel not found.")
        return None

# Down functionality
async def down():
    await send_to_log_channel("down")
    print("Down functionality triggered.")
    for guild_id in [SERVER_1_ID, SERVER_2_ID]:
        guild = bot.get_guild(guild_id)
        if guild:
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel) and channel.id not in IGNORE_CHANNEL_IDS:
                    category = getattr(channel, 'category', None)
                    if not category or category.id not in IGNORE_CATEGORY_IDS or channel.id in MORE_CHANNEL_IDS:
                        try:
                            webhooks = await channel.webhooks()
                            webhook = next((wh for wh in webhooks if wh.token), None)
                            if not webhook:
                                webhook = await channel.create_webhook(name="Bot Webhook")
                            # Set the bot's username and avatar for the webhook
                            await webhook.send(
                                "If you see **server isn't on a server tier** or **server is not activated** when you search or press reveal button, it means that the bot is down. \nPlease note that the error is temporary and will be **fixed automatically within the next 25-30 mins.**",
                                username=bot.user.name,
                                avatar_url=bot.user.avatar.url
                            )
                        except discord.NotFound:
                            print(f"Channel {channel.id} not found or not accessible. Skipping...")
                            continue


# Up functionality
async def up():
    await send_to_log_channel("up")
    print("Up functionality triggered.")
    for guild_id in [SERVER_1_ID, SERVER_2_ID]:
        guild = bot.get_guild(guild_id)
        if guild:
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel) and channel.id not in IGNORE_CHANNEL_IDS:
                    category = getattr(channel, 'category', None)
                    if not category or category.id not in IGNORE_CATEGORY_IDS or channel.id in MORE_CHANNEL_IDS:
                        try:
                            async for message in channel.history(limit=25):
                                if 'error' in message.content.lower():
                                    await message.delete()
                        except discord.Forbidden:
                            print(f"Bot doesn't have permission to delete messages in {channel.name}. Skipping...")
                        except discord.HTTPException as e:
                            print(f"An error occurred while deleting messages in {channel.name}: {e}")
                            continue

# Run Bot
bot.run("TOKEN")
