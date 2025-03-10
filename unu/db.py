import os
import sys
import logging
from pathlib import Path
from typing import Optional

from tortoise import Tortoise, connections, fields
from tortoise.backends.base.client import Capabilities
from tortoise.models import Model

# UTF-8 karakter kodlamasını zorla
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Veritabanı dizinini oluştur
DB_DIR = Path("./data")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "database.sqlite"

# Log dizinini oluştur
LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)

# Loglama ayarları
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Dosya handler'ı
file_handler = logging.FileHandler(
    LOG_DIR / "db.log",
    encoding='utf-8'
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(file_handler)

# Konsol handler'ı
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
)
logger.addHandler(console_handler)

class Chat(Model):
    id = fields.IntField(pk=True)
    theme = fields.CharField(max_length=255, default="classic")
    bluff = fields.BooleanField(default=True)
    seven = fields.BooleanField(default=False)
    one_win = fields.BooleanField(default=False)
    one_card = fields.BooleanField(default=False)
    lang = fields.CharField(max_length=255, default="tr-TR")  # Varsayılan dili Türkçe yaptık
    auto_pin = fields.BooleanField(default=False)
    satack = fields.BooleanField(default=True)
    draw_one = fields.BooleanField(default=True)


class User(Model):
    id = fields.BigIntField(pk=True)
    placar = fields.BooleanField(default=False)
    wins = fields.IntField(default=0)
    matches = fields.IntField(default=0)
    cards = fields.IntField(default=0)
    sudo = fields.BooleanField(default=False)
    lang = fields.CharField(max_length=255, default="tr-TR")  # Varsayılan dili Türkçe yaptık


class GameModel(Model):
    id = fields.IntField(pk=True)
    theme = fields.CharField(max_length=255)
    chat_id = fields.IntField(null=True)
    last_card = fields.JSONField(null=True)
    last_card_2 = fields.JSONField(null=True)
    next_player_id = fields.IntField(null=True)
    deck = fields.JSONField(null=True)
    players = fields.JSONField(null=True)
    is_started = fields.BooleanField(default=False)
    draw = fields.IntField(default=0)
    drawed = fields.BooleanField(default=False)
    chosen = fields.CharField(max_length=255, null=True)
    closed = fields.BooleanField(default=False)
    winner = fields.BooleanField(default=True)
    timer_duration = fields.IntField(default=30)
    message_id = fields.IntField(null=True)
    is_dev = fields.BooleanField(default=False)
    bluff = fields.BooleanField(default=False)


class GamePlayer(Model):
    player_id = fields.IntField()
    game_chat_id = fields.IntField()


async def init_db():
    """Veritabanı bağlantısını başlat ve şemayı oluştur"""
    try:
        logger.info("Veritabanına bağlanılıyor...")
        
        # SQLite veritabanı bağlantı URL'si
        db_url = f"sqlite://{DB_PATH}"
        
        # Tortoise ORM'yi başlat
        await Tortoise.init(
            db_url=db_url,
            modules={'models': ['unu.db']}
        )
        
        # SQLite özelliklerini ayarla
        conn = connections.get("default")
        conn.capabilities = Capabilities(
            "sqlite",
            daemon=False,
            requires_limit=True,
            inline_comment=True,
            support_for_update=False,
            support_update_limit_order_by=False,
        )
        
        # Veritabanı şemasını oluştur
        logger.info("Veritabanı şeması oluşturuluyor...")
        await Tortoise.generate_schemas(safe=True)
        
        logger.info("Veritabanı bağlantısı başarılı!")
        
    except Exception as e:
        logger.error(f"Veritabanı bağlantısında hata: {str(e)}")
        raise

async def close_db():
    """Veritabanı bağlantısını kapat"""
    try:
        await Tortoise.close_connections()
        logger.info("Veritabanı bağlantısı kapatıldı.")
    except Exception as e:
        logger.error(f"Veritabanı kapatılırken hata: {str(e)}")
        raise
