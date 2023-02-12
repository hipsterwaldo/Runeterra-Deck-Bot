import discord
from discord.ext import commands
import decksearch
from lor_deckcodes import LoRDeck
import pathlib
import image
from PIL import Image
import urllib.request

MAIN_DATA_PATH = pathlib.Path(r"B:\Eigene Dateien\desktop\bard bot\lor_decks")
all_sets = decksearch.load_all_sets(MAIN_DATA_PATH)

def run_discord_bot():
    with open("token.key") as f:
        TOKEN = f.read()
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
            sorted_deck = decksearch.sort_for_cost(deck, all_sets)
            url="https://runeterra.ar/decks/code/" + split_message[1]
            champions = decksearch.card_name_list_to_string(decksearch.get_champions(sorted_deck))
            units = decksearch.card_name_list_to_string(decksearch.get_units(sorted_deck))
            spells = decksearch.card_name_list_to_string(decksearch.get_spells(sorted_deck))
            other = decksearch.card_name_list_to_string(decksearch.get_other(sorted_deck))

            embed=discord.Embed(title="Decklink runeterra.ar", url=url)
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/leagueoflegends/images/2/2c/Legends_of_Runeterra_icon.png/revision/latest?cb=20191020214918")
            embed.add_field(name="Champions", value=champions, inline=True)
            embed.add_field(name="Follower", value=units, inline=True)
            embed.add_field(name="Spells", value=spells, inline=True)
            embed.add_field(name="Equipments and Landmarks", value=other, inline=True)

            await message.channel.send(embed=embed)

        if message.content.startswith("!card"):
            split_message = message.content.split(" ", 1)

            card_dictionary = decksearch.get_dictionary_of_card_name(split_message[1], all_sets)
            embed=discord.Embed(title=split_message[1].capitalize())
            urllib.request.urlretrieve(card_dictionary["assets"][0]["gameAbsolutePath"], "image1.png")
            b = Image.open("image1.png")

            if card_dictionary["associatedCardRefs"]:
                image_list = []
                image_list.append(b)
                for card_refs in card_dictionary["associatedCardRefs"]:
                    card_associats = decksearch.get_card_dictionary_of_card_code(card_refs, all_sets)
                    urllib.request.urlretrieve(card_associats["assets"][0]["gameAbsolutePath"], "image.png")
                    im = Image.open("image.png")
                    image_list.append(im)
                    image.merge_images(image_list)
                file = discord.File("B:/eigene dateien/desktop/runeterra deck bot/NewImage.jpg", filename="NewImage.jpg")
                embed.set_image(url="attachment://NewImage.jpg")
            else:
                embed.set_image(url=card_dictionary["assets"][0]["gameAbsolutePath"])

            await message.channel.send(file= file, embed=embed)

    client.run(TOKEN)
