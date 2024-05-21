import discord

# Spoofing information message
spoof_info_message = """Here are the safety ratings for each spoofing method-
* Tethering for Windows/Mac + iOS/Android (99% safe)
 * [click here](<https://discord.com/channels/864766766932426772/1190466821783027902>) for tethering guide for Android & iOS
* Jailbreak iOS + iPoGo/SpooferPro (95% safe)
 * [click here](<https://discord.com/channels/864766766932426772/1216550585961156619>) for Jailbreak Guide
 * [click here](<https://discord.com/channels/864766766932426772/1216579234567295070>) for SpooferPro Installation Guide
 * [click here](<https://ipogo.app/install.php#ios>) to find iPoGO Installation Guide
* Rooted Android Device + GPS Joystick by App Ninjas (95% safe)
 * [click here](<http://gpsjoystick.theappninjas.com/>) for installation guide by app ninjas.
* Rooted Android + Pokemod (85% safe)
 * [click here](<https://pokemod.dev/>) for guide
* Non-Rooted + PGSharp (65% safe)
 * [click here](<https://www.pgsharp.com/how-to-use-pgsharp-for-free/>) for PGSharp guide for normal android.
* Non-Jailbreak iOS + iPoGo (Unsafe)"""

cooldown_info_message = """A Cooldown is the amount of time you need to wait after using an in-game action. This is calculated from the distance you will travel between your in-game actions.
For more details, [click here](<https://discord.com/channels/864766766932426772/1234539731480481945>)"""

ptc_info_message = """You must link a PTC Account to your Pokemon GO Account to login without 2FA requirement.
Step 1: Open Pokemon GO
Step 2: Go to Pokemon GO Settings and scroll down until you find account.
Step 3: Click on it and link your Pokemon Trainer Club account"""

vip_info_message = """Here are the steps to get your VIP Trainer role once you purchase our subscription via Patreon-
[Click here](<https://support.patreon.com/hc/en-us/articles/212052266-Getting-Discord-access>) for discord access guide.
If you did follow the above guide correctly and still didn't get the VIP Trainer role, follow these steps-
* Step 1: Disconnect and Reconnect your Discord to the patreon. (Make sure you connect the correct discord account)
* Step 2: Click on the "Join Server" button that is shown in the membership page (you do **not** need to leave the server)
* Step 3: Wait for atleast 30 minutes after doing this. If you still didn't receive your role, then message - **<@972807243412152381>**"""

hotspots_info_message = """[Click here](<https://discord.com/channels/864766766932426772/1172095689531084842>) to find list of all hotspots coordinates."""

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'Guide')
# Initialize Discord client with intents

async def spoof_message_sent_recently(channel):
    async for message in channel.history(limit=75):
        if message.author == client.user and message.content == spoof_info_message:
            return True
    return False

async def ptc_message_sent_recently(channel):
    async for message in channel.history(limit=75):
        if message.author == client.user and message.content == ptc_info_message:
            return True
    return False

async def cooldown_message_sent_recently(channel):
    async for message in channel.history(limit=75):
        if message.author == client.user and message.content == cooldown_info_message:
            return True
    return False    

async def vip_message_sent_recently(channel):
    async for message in channel.history(limit=75):
        if message.author == client.user and message.content == vip_info_message:
            return True
    return False    

async def hotspots_message_sent_recently(channel):
    async for message in channel.history(limit=75):
        if message.author == client.user and message.content == hotspots_info_message:
            return True
    return False    

@client.event
async def on_message(message):
    # Check if the message is in one of the desired channels and starts with !spoof
    if message.content.startswith('!spoof'):
        # Check the last 75 messages for the bot's message
        if await spoof_message_sent_recently(message.channel):
            await message.channel.send("Guide message was already shared recently, scroll up the chat to find.")
        else:
            await message.channel.send(spoof_info_message)
    if message.content.startswith('!ptclink'):
        # Check the last 75 messages for the bot's message
        if await ptc_message_sent_recently(message.channel):
            await message.channel.send("Guide message was already shared recently, scroll up the chat to find.")
        else:
            await message.channel.send(ptc_info_message)
    if message.content.startswith('!cooldown'):
        # Check the last 75 messages for the bot's message
        if await cooldown_message_sent_recently(message.channel):
            await message.channel.send("Guide message was already shared recently, scroll up the chat to find.")
        else:
            await message.channel.send(cooldown_info_message)
    if message.content.startswith('!viprole'):
        # Check the last 75 messages for the bot's message
        if await vip_message_sent_recently(message.channel):
            await message.channel.send("Guide message was already shared recently, scroll up the chat to find.")
        else:
            await message.channel.send(vip_info_message)
    if message.content.startswith('!hotspot'):
        # Check the last 75 messages for the bot's message
        if await hotspots_message_sent_recently(message.channel):
            await message.channel.send("Guide message was already shared recently, scroll up the chat to find.")
        else:
            await message.channel.send(hotspots_info_message)

# Run the bot
client.run("TOKEN")
