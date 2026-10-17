import os
import staypresent

# Код твоего бота остается в bot.py, мы его не трогаем
# StayPresent запускает bot.py и держит порт открытым для Koyeb
staypresent.run(
    "bot.py",
    port=int(os.getenv("PORT", 8080))
)
