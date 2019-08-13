import discord
from discord.ext import commands
import json
import asyncio

class levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.loop.create_task(self.seve_users())


        with open(r"data/users.json", 'r') as f:
            self.users = json.load(f)

    async def seve_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"data/users.json", 'w') as f:
                json.dump(self.users, f, indent=4)

            await asyncio.sleep(5)



    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        author_id = str(message.author.id)

    def lvl_up(self, author_id):
        cur_xp = self.users[author_id]['exp']
        cuz_lvl = self.users[author_id]['level']

        if cur_xp >= round((4 * (cuz_lvl ** 3)) / 5):
            self.users[author_id]['level'] += 1
            return True
        else:
            return False





        

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)

        embed = discord.Embed(color=member.color, timestap=ctx.message.created_at)

        embed.set_author(name=f"Rank - {member}", icon_url=self.bot.user.avatar_url)

        embed.add_field(name="Level", value=self.users[member_id]['level'])
        embed.add_field(name="XP", value=self.users[member_id]['exp'])

        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        author_id = str(message.author.id)

        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]['level'] = 1
            self.users[author_id]['exp'] = 0

        self.users[author_id]['exp'] += 1
        
        if self.lvl_up(author_id):
            await message.channel.send(f"{message.author.mention} is now level {self.users[author_id]['level']}'")


def setup(bot):
    bot.add_cog(levels(bot))
