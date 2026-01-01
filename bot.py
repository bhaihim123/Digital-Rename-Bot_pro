# (c) @RknDeveloperr
# Rkn Developer 
# Don't Remove Credit 😔

import aiohttp
import warnings
import pytz
import datetime
import logging
import glob, sys
import importlib.util
from pathlib import Path

from pyrogram import Client, __version__
from pyrogram.raw.all import layer

from config import Config
from plugins.web_support import web_server
from plugins.file_rename import app

# ================= LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("BotLog.txt"),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# ================= BOT CLASS =================
class DigitalRenameBot(Client):
    def __init__(self):
        super().__init__(
            name="DigitalRenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=5,
            max_concurrent_transmissions=50
        )

    async def start(self):
        await super().start()

        me = await self.get_me()
        Config.BOT = self

        # ✅ REQUIRED ATTRIBUTES (PLUGIN FIX)
        self.premium = Config.PREMIUM_MODE
        self.uploadlimit = Config.UPLOAD_LIMIT_MODE

        # Web server
        runner = aiohttp.web.AppRunner(await web_server())
        await runner.setup()
        await aiohttp.web.TCPSite(runner, "0.0.0.0", Config.PORT).start()

        # Load plugins manually
        for file in glob.glob("plugins/*.py"):
            path = Path(file)
            name = path.stem
            spec = importlib.util.spec_from_file_location(f"plugins.{name}", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[f"plugins.{name}"] = module
            print("Loaded plugin:", name)

        print(f"{me.first_name} Started Successfully ✅")

        # Notify admins
        for admin in Config.ADMIN:
            try:
                await self.send_message(
                    admin,
                    f"**{me.first_name} Bot Started Successfully 🚀**"
                )
            except:
                pass

        # Log channel
        if Config.LOG_CHANNEL:
            try:
                now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"**Bot Restarted**\n\n"
                    f"📅 {now.strftime('%d %B %Y')}\n"
                    f"⏰ {now.strftime('%I:%M:%S %p')}\n"
                    f"🧩 Pyrogram v{__version__} (Layer {layer})"
                )
            except:
                pass

    async def stop(self, *args):
        for admin in Config.ADMIN:
            try:
                await self.send_message(admin, "**Bot Stopped ❌**")
            except:
                pass
        await super().stop()

# ================= RUN BOT =================
warnings.filterwarnings("ignore")

digital_bot = DigitalRenameBot()

# 🔥 Deepnote + VPS safe
digital_bot.run()
