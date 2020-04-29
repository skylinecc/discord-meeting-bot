import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user:
            return

        elif message.content.startswith('-help') or message.content.startswith('-info'):
            await message.channel.send('To see this list of commands, type `-help` or `-info`\nTo get the information for the next Zoom meeting, type `-nextmeeting`')

        elif message.content.startswith('-nextmeeting'):
            await message.channel.send('Temporary next meeting message (WIP)')

        elif message.content.startswith('-'):
            await message.channel.send('Hello! I\'m a Discord bot <@449579826278563860> made!\nMy prefix is `-`\nFor a list of commands, type `-help` or `-info`')


client = MyClient()
client.run('NzA0ODY5NjIxMDg5Njk3ODUz.Xqjbcg.CLRqjFE0N08BdBV6tDkyxS5_KUc')
