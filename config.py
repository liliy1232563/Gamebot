import logging
import importlib

from telegram import BotCommand
from telegram.ext import Application

from config import (
BOT_TOKEN,
BOT_NAME,
SET_COMMANDS,
)

============================================================

LOGGING

============================================================

logging.basicConfig(
format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
level=logging.INFO,
)

logger = logging.getLogger("solurix")

============================================================

TELEGRAM COMMAND MENU

============================================================

COMMANDS = [
BotCommand("start", "Start Solurix"),
BotCommand("help", "Show all commands"),
BotCommand("profile", "View your profile"),
BotCommand("stats", "View your statistics"),
BotCommand("rank", "View group ranking"),
BotCommand("daily", "Claim your daily reward"),
BotCommand("weekly", "Claim your weekly reward"),
BotCommand("battle", "Start a battle"),
BotCommand("hunt", "Go on a hunt"),
BotCommand("train", "Train your character"),
BotCommand("explore", "Explore the world"),
BotCommand("coins", "Check your coins"),
BotCommand("level", "Check your level"),
BotCommand("history", "View recent game activity"),
BotCommand("support", "Open Solurix support"),
]

============================================================

COMMAND SETUP

============================================================

async def setup_commands(application: Application) -> None:
"""Register Telegram command suggestions."""

if not SET_COMMANDS:
    logger.info("Telegram command menu setup disabled.")
    return

await application.bot.set_my_commands(COMMANDS)

logger.info(
    "Telegram command menu configured for %s.",
    BOT_NAME,
)

============================================================

PLUGIN LOADER

============================================================

def load_plugins(application: Application) -> None:
"""Import and register available plugins."""

plugin_names = [
    "start",
    "help",
    "game",
    "profile",
    "ranking",
    "daily",
    "weekly",
    "battle",
    "hunt",
    "admin",
    "auto_reply",
    "coins",
    "stats",
    "level",
    "history",
    "explore",
    "train",
]

loaded = 0
failed = 0

for plugin_name in plugin_names:
    try:
        module = importlib.import_module(
            f"plugins.{plugin_name}"
        )

        setup = getattr(module, "setup", None)

        if not callable(setup):
            logger.warning(
                "Plugin %s has no callable setup() function.",
                plugin_name,
            )
            continue

        setup(application)
        loaded += 1

        logger.info("Loaded plugin: %s", plugin_name)

    except ModuleNotFoundError as exc:
        # Skip only when the plugin itself is missing.
        # Dependencies missing inside a plugin must be reported.
        if exc.name in (
            f"plugins.{plugin_name}",
            "plugins",
        ):
            logger.warning(
                "Plugin not found: %s",
                plugin_name,
            )
        else:
            failed += 1
            logger.exception(
                "Missing dependency while loading plugin %s: %s",
                plugin_name,
                exc.name,
            )

    except Exception:
        failed += 1
        logger.exception(
            "Failed to load plugin: %s",
            plugin_name,
        )

logger.info(
    "Plugin loading finished: %s loaded, %s failed.",
    loaded,
    failed,
)

============================================================

MAIN

============================================================

def main() -> None:
"""Build and run the Solurix Telegram bot."""

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing. Set it in the hosting environment."
    )

logger.info("Starting %s...", BOT_NAME)

application = (
    Application.builder()
    .token(BOT_TOKEN)
    .post_init(setup_commands)
    .build()
)

load_plugins(application)

logger.info("Starting Telegram long polling...")

application.run_polling()

============================================================

ENTRY POINT

============================================================

if name == "main":
try:
main()
except KeyboardInterrupt:
logger.info("Bot stopped manually.")
except Exception:
logger.exception("Bot startup or runtime failed.")
raise