import discord
from discord.ext import commands
import decksearch
from lor_deckcodes import LoRDeck

def run_discord_bot():
    TOKEN = 'Insert Discord Token here'
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix="!",  intents=intents)


    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    
    @client.event
    async def on_message(message):

        if message.content.startswith("!deck"):
            
            split_message = message.content.split()
            deck = LoRDeck.from_deckcode(split_message[1])
            sorted_deck = decksearch.sort_for_cost(deck)
            url="https://runeterra.ar/decks/code/" + split_message[1]
            champions = decksearch.card_list_to_string(decksearch.get_champions(sorted_deck))
            units = decksearch.card_list_to_string(decksearch.get_units(sorted_deck))
            spells = decksearch.card_list_to_string(decksearch.get_spells(sorted_deck))
            other = decksearch.card_list_to_string(decksearch.get_other(sorted_deck))

            embed=discord.Embed(title="Decklink runeterra.ar", url=url)
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/leagueoflegends/images/2/2c/Legends_of_Runeterra_icon.png/revision/latest?cb=20191020214918")
            embed.add_field(name="Champions", value=champions, inline=True)
            embed.add_field(name="Units", value=units, inline=True)
            embed.add_field(name="Spells", value=spells, inline=True)
            embed.add_field(name="Equipments and Landmarks", value=other, inline=True)

            await message.channel.send(embed=embed)

        if message.content.startswith("!card"):
            split_message = message.content.split(" ", 2)
            print(split_message)
            url = decksearch.get_url_path(split_message[1])

            embed=discord.Embed(title=split_message[1].capitalize())
            embed.set_image(url=url)
            await message.channel.send(embed=embed)

    
    client.run(TOKEN)
