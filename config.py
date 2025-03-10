import os
from dotenv import load_dotenv
from hydrogram import Client, filters
from hydrogram.enums import ParseMode
from functools import wraps

# .env dosyasını yükle
load_dotenv()

# Komut öneki
CMD_PREFIX = "/"

# Filtreler
cmd_filter = filters.group | filters.private

# Oyun durumlarını tutan sözlükler
games = {}
player_game = {}

# Oyun ayarları
timeout = 120  # Oyuncu başına süre (saniye)
minimum_players = 2  # Minimum oyuncu sayısı

# Yönetici listesi - güvenlik için environment variable'dan alınmalı
ADMIN_IDS = os.getenv("UNO_ADMIN_IDS", "").split(",")
sudoers = [int(admin_id.strip()) for admin_id in ADMIN_IDS if admin_id.strip()]

# API bilgileri
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("Telegram API bilgileri eksik! Lütfen environment variable'ları kontrol edin.")

# API_ID'yi integer'a çevir
try:
    API_ID = int(API_ID)
except (TypeError, ValueError):
    raise ValueError("TELEGRAM_API_ID geçerli bir sayı olmalıdır!")

# Bot istemcisi
bot = Client(
    "uno_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="unu.plugins"),
    # Webhook parametrelerini kaldırdım
    in_memory=True,
    workers=6,
)

# Rate limiting ayarları
MAX_REQUESTS_PER_SECOND = 20  # Saniye başına maksimum istek sayısını düşür
MAX_CONCURRENT_GAMES = 50  # Eşzamanlı oyun sayısını sınırla

# Güvenlik ayarları
ALLOWED_CHAT_TYPES = ["group", "supergroup"]  # Sadece gruplarda çalış
MAX_PLAYERS_PER_GAME = 10  # Oyun başına maksimum oyuncu
MAX_GAMES_PER_USER = 1  # Kullanıcı başına maksimum aktif oyun

# Komut işleyici dekoratörü
def command(commands):
    """Komut işleyici dekoratörü"""
    if isinstance(commands, str):
        commands = [commands]
    
    def decorator(func):
        @wraps(func)
        async def wrapper(client, message, *args, **kwargs):
            try:
                return await func(client, message, *args, **kwargs)
            except Exception as e:
                import logging
                logging.getLogger('root').error(f"Komut işlenirken hata: {e}")
                try:
                    await message.reply(f"Komut işlenirken bir hata oluştu: {e}", quote=True)
                except:
                    pass
        
        # Komut filtresi oluştur
        command_filter = filters.command(commands) & cmd_filter
        
        # Dekoratörü uygula
        return bot.on_message(command_filter)(wrapper)
    
    return decorator 