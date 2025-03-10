import os
import asyncio
import logging
from dotenv import load_dotenv
from tortoise import Tortoise

# .env dosyasını yükle
load_dotenv()

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('db_migrate')

# Veritabanı URL'leri
SQLITE_URL = "sqlite://./data/database.sqlite"
POSTGRES_URL = os.getenv("DATABASE_URL")

async def migrate_data():
    """SQLite'dan PostgreSQL'e veri taşıma"""
    if not POSTGRES_URL or POSTGRES_URL.startswith("sqlite://"):
        logger.error("PostgreSQL URL'si bulunamadı veya geçersiz!")
        return
    
    # PostgreSQL URL'sini düzelt
    postgres_url = POSTGRES_URL
    if postgres_url.startswith("postgres://"):
        postgres_url = postgres_url.replace("postgres://", "postgresql://", 1)
    
    logger.info("SQLite veritabanına bağlanılıyor...")
    await Tortoise.init(
        db_url=SQLITE_URL,
        modules={"models": ["unu.db"]}
    )
    
    # Verileri al
    from unu.db import User, Chat, GameModel, GamePlayer
    
    logger.info("Verileri alınıyor...")
    users = await User.all()
    chats = await Chat.all()
    games = await GameModel.all()
    players = await GamePlayer.all()
    
    logger.info(f"Alınan veriler: {len(users)} kullanıcı, {len(chats)} sohbet, {len(games)} oyun, {len(players)} oyuncu")
    
    # SQLite bağlantısını kapat
    await Tortoise.close_connections()
    
    # PostgreSQL'e bağlan
    logger.info("PostgreSQL veritabanına bağlanılıyor...")
    await Tortoise.init(
        db_url=postgres_url,
        modules={"models": ["unu.db"]}
    )
    
    # Şemayı oluştur
    logger.info("PostgreSQL şeması oluşturuluyor...")
    await Tortoise.generate_schemas()
    
    # Verileri taşı
    logger.info("Veriler PostgreSQL'e taşınıyor...")
    
    # Kullanıcıları taşı
    for user in users:
        try:
            await User.create(
                id=user.id,
                lang=user.lang,
                # Diğer alanları da ekleyin
            )
        except Exception as e:
            logger.error(f"Kullanıcı taşınırken hata: {e}")
    
    # Sohbetleri taşı
    for chat in chats:
        try:
            await Chat.create(
                id=chat.id,
                lang=chat.lang,
                theme=chat.theme,
                # Diğer alanları da ekleyin
            )
        except Exception as e:
            logger.error(f"Sohbet taşınırken hata: {e}")
    
    # Oyunları ve oyuncuları taşıma işlemi daha karmaşık olabilir
    # Burada sadece temel bir örnek gösteriyoruz
    
    logger.info("Veri taşıma işlemi tamamlandı!")
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(migrate_data()) 