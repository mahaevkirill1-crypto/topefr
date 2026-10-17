import andro_cfw

# Этот патч перенаправляет все запросы бота через Cloudflare
session = andro_cfw.patch()

# Запускаем твой существующий bot.py
import bot
