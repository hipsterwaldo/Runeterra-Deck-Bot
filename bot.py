import discord
from discord.ext import commands
import decksearch
from lor_deckcodes import LoRDeck
import pathlib
from PIL import Image
import io
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
            champions = decksearch.card_list_to_string(decksearch.get_champions(sorted_deck))
            units = decksearch.card_list_to_string(decksearch.get_units(sorted_deck))
            spells = decksearch.card_list_to_string(decksearch.get_spells(sorted_deck))
            other = decksearch.card_list_to_string(decksearch.get_other(sorted_deck))

            embed=discord.Embed(title="Decklink runeterra.ar", url=url)
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/leagueoflegends/images/2/2c/Legends_of_Runeterra_icon.png/revision/latest?cb=20191020214918")
            embed.add_field(name="Champions", value=champions, inline=True)
            embed.add_field(name="Follower", value=units, inline=True)
            embed.add_field(name="Spells", value=spells, inline=True)
            embed.add_field(name="Equipments and Landmarks", value=other, inline=True)

            await message.channel.send(embed=embed)

        if message.content.startswith("!card"):
            split_message = message.content.split(" ")

            associats = decksearch.get_dictionary_of_card_name(split_message[1], all_sets)
            embed=discord.Embed(title=split_message[1].capitalize())
            urllib.request.urlretrieve(associats["assets"][0]["gameAbsolutePath"], "image1.png")
            b = Image.open("image1.png")

            if associats["associatedCardRefs"]:
                
                im_list = []
                im_list.append(b)
                for cards in associats["associatedCardRefs"]:
                    card = decksearch.get_card_dictionary_of_card_CODE(cards, all_sets)
                    urllib.request.urlretrieve(card["assets"][0]["gameAbsolutePath"], "image.png")
                    im = Image.open("image.png")
                    im_list.append(im)
                    merge_images(im_list)
                
                file = discord.File("B:/eigene dateien/desktop/runeterra deck bot/NewImage.jpg", filename="NewImage.jpg")
                embed.set_image(url="attachment://NewImage.jpg")
            else:
                embed.set_image(url=associats["assets"][0]["gameAbsolutePath"])

            
            await message.channel.send(file= file, embed=embed)

    
    client.run(TOKEN)


def merge_images(image_list):
        # Open images and store them in a list
    total_width = 0
    max_height = 0
    # find the width and height of the final image
    for img in image_list:
        total_width += img.size[0]
        max_height = max(max_height, img.size[1])
    # create a new image with the appropriate height and width
    new_img = Image.new('RGB', (total_width, max_height))
    # Write the contents of the new image
    current_width = 0
    for img in image_list:
        new_img.paste(img, (current_width,0))
        current_width += img.size[0]
    # Save the image
    new_img.save('NewImage.jpg')
