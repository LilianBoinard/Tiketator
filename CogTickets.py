import discord
from discord.ext import commands
import discord.utils
import TicketsJSON
import asyncio
import os


class CogTickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Main command
    @commands.command()
    async def tickets(self, ctx, action, *args):

        ticket_author = ctx.author

        match action:
            case 'add':
                ticket_content = ' '.join(args)
                await self.add_ticket(ticket_author, ticket_content)
            case 'list':
                await CogTickets.get_ticket_list(ticket_author)
            case 'git':
                await CogTickets.git(ctx.author)
        return

    async def annouce_result(self, ticket_id):

        close_channel = int(os.getenv('close_channel'))

        tickets = TicketsJSON.get_tickets_json()
        result = tickets[ticket_id]['results']

        title = "Ticket Refusé ❌"
        color = 0xb8122b

        if result['for'] > result['against']:
            title = "Ticket Intégré ✅"
            color = 0x26d454

        # Embed ticket
        embed = discord.Embed(title=f"**{title}**", colour=color)
        embed.add_field(name='', value=f'Auteur: **@{tickets[ticket_id]["author"]}**', inline=False)
        embed.add_field(name='', value=f'Idée: **{tickets[ticket_id]["content"]}**', inline=False)

        await self.bot.get_channel(close_channel).send(embed=embed)

    @staticmethod
    async def git(author):
        embed = discord.Embed(title="**Git of Tiketator**", colour=0x595959)
        embed.add_field(name='', value='https://github.com/LilianBoinard/Tiketator')

        await author.send(embed=embed)

    async def announce_open_ticket(self, ticket_id):

        tickets = TicketsJSON.get_tickets_json()
        open_channel = int(os.getenv('open_channel'))

        # Embed ticket
        embed = discord.Embed(title="**Nouveau Ticket**", colour=0x595959)
        embed.add_field(name='', value=f'Auteur: **@{tickets[ticket_id]["author"]}**', inline=False)
        embed.add_field(name='', value=f'Idée: **{tickets[ticket_id]["content"]}**', inline=False)
        embed.set_footer(text='Réagis avec ✅ ou ❌')

        message = await self.bot.get_channel(open_channel).send(embed=embed)

        await asyncio.sleep(5)

        cache_msg = discord.utils.get(self.bot.cached_messages, id=message.id)

        ticket_for = 0 if not discord.utils.get(cache_msg.reactions, emoji='✅') else discord.utils.get(
            cache_msg.reactions, emoji='✅').count
        ticket_against = 0 if not discord.utils.get(cache_msg.reactions, emoji='❌') else discord.utils.get(
            cache_msg.reactions, emoji='❌').count

        tickets[ticket_id]['results'] = {"for": ticket_for, "against": ticket_against}
        tickets[ticket_id]['status'] = "fermé"

        TicketsJSON.dump_tickets_json(tickets)

        await message.delete()

        return await self.annouce_result(ticket_id)

    async def add_ticket(self, ticket_author, ticket_content):

        tickets = TicketsJSON.get_tickets_json()
        ticket_id = str((len(tickets) + 1))

        # Add new ticket json
        tickets[ticket_id] = {
            "author": ticket_author.name,
            "content": ticket_content,
            "results": {
                "for": 0,
                "against": 0
            },
            "status": "ouvert"}
        TicketsJSON.dump_tickets_json(tickets)

        await self.announce_open_ticket(ticket_id)

    @staticmethod
    async def get_ticket_list(ticket_author):

        tickets = TicketsJSON.get_tickets_json()

        # Embed tickets list
        embed = discord.Embed(title="**Liste des Tickets**", colour=0x595959)
        for ticket in tickets:
            embed.add_field(name='', value=f'Auteur: **@{tickets[ticket]["author"]}**', inline=False)
            embed.add_field(name='', value=f'Idée: **{tickets[ticket]["content"]}**', inline=False)
            embed.add_field(name='',
                            value=f'✅: **{tickets[ticket]["results"]["for"]}** ❌: **{tickets[ticket]["results"]["against"]}**',
                            inline=False)
            embed.add_field(name='', value=f'Status: **{tickets[ticket]["status"]}**', inline=False)
            embed.add_field(name='', value='\u200B')

        await ticket_author.send(embed=embed)

    # Credits
    @commands.command()
    async def tiketator(self, ctx):
        """ Embed de Tiketator """
        embed = discord.Embed(title="**TiketatorBOT**", description="created with ❤", colour=0x32a852)
        embed.set_author(name="liliangg",
                         icon_url="https://cdn.discordapp.com/avatars/494220268076662795/fe3dc477e9c165ac49b532729a0a175d.png")
        embed.set_footer(
            icon_url="https://cdn.discordapp.com/app-icons/1173720436115251311/74468ff618ccb6ab682ba5d8f1f48889.png?size=128",
            text="2023")
        await ctx.send(embed=embed)
