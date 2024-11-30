<!-- SPDX-License-Identifier: MIT -->

[![Disnake Banner](https://raw.githubusercontent.com/DisnakeDev/disnake/master/assets/banner.png)](https://disnake.dev/)

disnake-DVM F0rk of disnake
=======

A modern, easy to use, feature-rich, and async-ready API wrapper for Discord written in Python.

Key Features
------------

- Proper rate limit handling.
- Type-safety measures.
- [FastAPI](https://fastapi.tiangolo.com/)-like slash command syntax.

Voice Messages
--------------
#Slash and Context Menu Commands Example

```py
import disnake
import disnake.discordvm
from disnake.ext import commands
intents = disnake.Intents.all()
bot = commands.InteractionBot(intents=intents)
vm = disnake.discordvm.VoiceMessage(bot=bot)
@bot.message_command(name="Voice")
async def voice_ctx(inter: disnake.MessageCommandInteraction, message: disnake.Message):
    await inter.response.defer()
    await inter.channel.purge(limit=1) #type: ignore
    for audio in message.attachments:
        await vm.send(file=audio, channel_id=inter.channel_id)

@bot.slash_command(name="voice")
async def voice(ctx: disnake.ApplicationCommandInteraction, audio: disnake.Attachment):
    await ctx.response.defer()
    await ctx.channel.purge(limit=1) #type: ignore
    await vm.send(file=audio, channel_id=ctx.channel_id)

if __name__ == '__main__':
    bot.run(token)
```

Quick Example
-------------

### Slash Commands Example

``` py
import disnake
from disnake.ext import commands

bot = commands.InteractionBot(test_guilds=[12345])

@bot.slash_command()
async def ping(inter):
    await inter.response.send_message("Pong!")

bot.run("BOT_TOKEN")
```

### Context Menus Example

``` py
import disnake
from disnake.ext import commands

bot = commands.InteractionBot(test_guilds=[12345])

@bot.user_command()
async def avatar(inter, user):
    embed = disnake.Embed(title=str(user))
    embed.set_image(url=user.display_avatar.url)
    await inter.response.send_message(embed=embed)

bot.run("BOT_TOKEN")
```

### Prefix Commands Example

``` py
import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run("BOT_TOKEN")
```

You can find more examples in the [examples directory](https://github.com/sdkmasteri/disnake-DVM/tree/master/examples).

<br>
<p align="center">
    <a href="https://docs.disnake.dev/">Documentation</a>
    ⁕
    <a href="https://guide.disnake.dev/">Guide</a>
    ⁕
    <a href="https://discord.gg/disnake">Discord Server</a>
    ⁕
    <a href="https://discord.gg/discord-developers">Discord Developers</a>
</p>
<br>
