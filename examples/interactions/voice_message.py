import disnake
import disnake.discordvm
from disnake.ext import commands
intents = disnake.Intents.all()
bot = commands.InteractionBot(intents=intents)
bot.load_extensions("cogs")
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