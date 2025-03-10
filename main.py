import os
import sys
import signal
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from contextlib import suppress

from config import bot
from unu.db import init_db, close_db

# UTF-8 karakter kodlamasını zorla
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Ana logger'ı yapılandır
logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

# Dosya handler'ı
os.makedirs('logs', exist_ok=True)
file_handler = RotatingFileHandler(
    'logs/bot.log',
    maxBytes=1024 * 1024,  # 1MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(logging.DEBUG)  # DEBUG seviyesine düşürdüm
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(file_handler)

# Konsol handler'ı
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter('INFO: %(message)s')
)
logger.addHandler(console_handler)

# Global değişkenler
stop_event = asyncio.Event()

# Telegram API limitleri için yapılandırma
TELEGRAM_FLOOD_WAIT_SECONDS = 1  # Flood wait için bekleme süresi

async def shutdown():
    """Bot'u güvenli bir şekilde kapatır."""
    logger.info("Bot kapatılıyor...")
    
    # Tüm görevleri iptal et
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
    
    # Veritabanı bağlantısını kapat
    await close_db()
    
    # Bot'u durdur
    await bot.stop()
    
    # Stop event'i ayarla
    stop_event.set()
    
    logger.info("Bot başarıyla kapatıldı.")

def signal_handler(signum, frame):
    """Sinyal işleyicisi."""
    logger.info(f"Sinyal alındı: {signum}")
    
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(shutdown())
    else:
        loop.run_until_complete(shutdown())

# Gelen tüm mesajları logla
@bot.on_message()
async def debug_messages(client, message):
    """Gelen tüm mesajları logla."""
    try:
        logger.debug(f"Mesaj alındı: {message.text} | Chat ID: {message.chat.id} | User ID: {message.from_user.id if message.from_user else 'Bilinmiyor'}")
        
        # Komut mu kontrol et
        if message.text and message.text.startswith('/'):
            command = message.text.split()[0].split('@')[0]
            logger.debug(f"Komut alındı: {command}")
    except Exception as e:
        logger.error(f"Mesaj işlenirken hata oluştu: {e}")

# Callback query'leri logla
@bot.on_callback_query()
async def debug_callback(client, callback_query):
    """Gelen tüm callback query'leri logla."""
    try:
        logger.debug(f"Callback query alındı: {callback_query.data} | User ID: {callback_query.from_user.id}")
    except Exception as e:
        logger.error(f"Callback query işlenirken hata oluştu: {e}")

async def idle():
    """Bot'un çalışmaya devam etmesini sağlar."""
    while not stop_event.is_set():
        await asyncio.sleep(1)

async def main():
    """Ana fonksiyon."""
    try:
        # Sinyalleri yakala
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Veritabanını başlat
        await init_db()
        logger.info("Veritabanı başlatıldı")
        
        # Bot'u başlat
        logger.info("Bot başlatılıyor...")
        await bot.start()
        logger.info("Bot başlatıldı")
        
        # Bot bilgilerini al ve logla
        me = await bot.get_me()
        logger.info(f"Bot hazır! Kullanıcı adı: @{me.username}")
        
        # Bot çalışmaya devam etsin
        await idle()
    except Exception as e:
        logger.error(f"Ana fonksiyonda hata: {e}")
    finally:
        # Bot'u kapat
        await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Klavye kesintisi ile durduruldu")
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
    finally:
        logger.info("Program sonlandırıldı") 