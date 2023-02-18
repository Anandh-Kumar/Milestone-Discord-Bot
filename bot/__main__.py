from discord import Intents, Activity, ActivityType
from dotenv import load_dotenv
from json import load
from os import getenv


from bot.bot import Bot


load_dotenv()

with open(getenv("JSON_PATH"), "r", encoding="UTF-8") as json_file:
    CONSTANTS = load(json_file)


intents = Intents.all()

bot = Bot(
    command_prefix=CONSTANTS["BOT_CONSTANTS"]["COMMAND_PREFIX"],
    intents=intents,
    activity=Activity(type=ActivityType.watching, name="Best Bot (season 1)"),
    help_command=None,
)
bot.CONSTANTS = CONSTANTS
bot.run(CONSTANTS["BOT_CONSTANTS"]["TOKEN"])
