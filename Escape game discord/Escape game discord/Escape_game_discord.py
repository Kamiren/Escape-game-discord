import discord
import asyncio


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('---------')
        self.player_list = []
        self.player_id=[]
        self.channels = []
        self.state = 0

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if message.content.startswith('Escapebot') and self.state == 0:
            self.state = 1
            self.lancement = await message.channel.send('Qui participe ? ( utilise les réactions )')
            await self.lancement.add_reaction('🆙')
            await client.change_presence(activity=discord.Game(name='Creating Escape Game party !'))

    async def on_reaction_add(self, reaction, user):
        if user != self.user:
            if reaction.emoji == '🆙' and self.state == 1:
                if user.name in self.player_list:
                    await reaction.message.channel.send('Tu es déjà dans la party !')
                else:
                    self.player_list.append(user.name)
                    self.player_id.append(user.id)
                    print(self.player_list, self.player_id)
                    await reaction.message.channel.send('Il y a {} qui vient de rejoindre la party'.format(user.name))
                if len(self.player_list) == 1:
                    await reaction.message.channel.send('Un joueur sur quatre !')
                if len(self.player_list) == 2:
                    await reaction.message.channel.send('Deux joueurs sur quatre !')
                if len(self.player_list) == 3:
                    await reaction.message.channel.send('Trois joueurs sur quatre !')
                if len(self.player_list) >= 4:
                    await self.create_channel(reaction.message.guild)
                    await reaction.message.channel.send('Quatre joueurs sur quatre ! \n Nous allons débuter !')
                    self.state = 2
                    
    async def create_channel(self, guild):
       perm = {guild.default_role: discord.PermissionOverwrite(read_messages=False),
              guild.get_member(self.player_id[0]):
               discord.PermissionOverwrite(read_messages=True),
              guild.get_member(self.player_id[1]):
               discord.PermissionOverwrite(read_messages=True),
              guild.get_member(self.player_id[2]):
               discord.PermissionOverwrite(read_messages=True),
              guild.get_member(self.player_id[3]):
               discord.PermissionOverwrite(read_messages=True)}
       test = await guild.create_text_channel('Salle principale', overwrites=perm, position=0, reason='Start Escape game', nsfw=False)
       self.channels.append(test)
       await self.channels[0].send("")



client = MyClient()
client.run()