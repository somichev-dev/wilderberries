import random
import time
import tomllib
import discord
from product import get_random_id, Product, ProductNotFoundException

DESTINATION_CHANNEL = None
SEARCH_THRESHOLD = None

bot = discord.Client(intents=discord.Intents.default())

def get_random_product():
    product = None
    c = SEARCH_THRESHOLD
    while c > 0:
        try:
            product_id = get_random_id()
            product = Product(product_id)
            return product
        except ProductNotFoundException:
            c-=1
            print(f"не нашли продукт {product_id}, до конца поиска {c} попыток")
            time.sleep(5)
        except Exception as e:
            print(f"failed product id {product_id}")
            raise e
    return None

@bot.event
async def on_ready():
    print(f"Bot is ready and running as {bot.user}")
    product = get_random_product()
    ## this is a failure path
    if product == None:
        await bot.get_channel(DESTINATION_CHANNEL).send(":(")
        exit()
    embed = await construct_embed(product)
    try:
        await bot.get_channel(DESTINATION_CHANNEL).send(embed=embed)
    except discord.errors.HTTPException as e:
        print(f"failed product id {product._product_id}")
        print(product.thumbanil_link)
        raise e
    await bot.close()

async def construct_embed(product: Product) -> discord.Embed:
    embed=discord.Embed(
        title=product.name,
        url=product.product_link,
        color=0x1a5fb4
    )
    embed.set_author(name="товар дня вб ру")
    embed.add_field(
        name="Рейтинг",
        value=f"{product.rating} :star: ({product.rating_amount})", inline=True
    )
    embed.add_field(name="Цена", value=product.cost, inline=True)
    embed.set_image(url=product.thumbnail_link)
    with open("flavors.txt", "r", encoding="utf-8") as f:
        embed.set_footer(text=random.choice(f.readlines()).rstrip('\n'))
    return embed

def main():
    global DESTINATION_CHANNEL, SEARCH_THRESHOLD
    config = tomllib.load(open("config.toml", "rb"))
    token = config["token"]
    DESTINATION_CHANNEL = config["channel"]
    SEARCH_THRESHOLD = config["threshold"]
    bot.run(token)

if __name__ == "__main__":
    main()