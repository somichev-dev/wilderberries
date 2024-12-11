import discord
from discord.ext import commands
import random, time
from product import MAX_PRODUCT_ID, Product, CaptchaException, ProductNotFoundException

DESTINATION_CHANNEL = 1316185782335307826
SEARCH_THRESHOLD = 10

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

def get_random_product():
    product = None
    c = SEARCH_THRESHOLD
    while c > 0:
        try:
            product_id = random.randint(1, MAX_PRODUCT_ID)
            product = Product(product_id)
            return product
        except CaptchaException:
            print("КАПЧА КАПЧА АХУТНГ АХТУНГ КАПЧА НАДО ОБНОВИТЬ КУКИ НАМ ВСЕМ ПИЗДЕЦ")
            return None
        except ProductNotFoundException:
            c-=1
            print(f"не нашли продукт {product_id}, до конца поиска {c} попыток")
            time.sleep(1 + random.randint(0, 3))
        except Exception as e:
            print(f"failed product id {product_id}")
            raise e
            return None
    return None

@bot.event
async def on_ready():
    print(f"Bot is ready and running as {bot.user}")
    product = get_random_product()
    ## this is a failure path
    if product == None:
        await bot.get_channel(DESTINATION_CHANNEL).send(":(")
        exit()
    ## this is a happy path
    embed=discord.Embed(
        title=product.name,
        url=product.product_link,
        color=0x1a5fb4
    )
    embed.set_author(name="товар дня озон ру")
    embed.add_field(
        name="Рейтинг",
        value=f"{product.rating} :star: ({product.rating_amount})", inline=True
    )
    embed.add_field(name="Цена", value=product.cost, inline=True)
    embed.set_image(url=product.thumbnail_link)
    await bot.get_channel(DESTINATION_CHANNEL).send(embed=embed)
    await bot.close()

with open("token", "r") as f:
    token = f.read()
    bot.run(token)