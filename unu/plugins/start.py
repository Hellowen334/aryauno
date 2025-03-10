from hydrogram import Client, filters
from hydrogram.types import Message, CallbackQuery
from hydrogram.helpers import ikb
import logging

from unu.db import User
from unu.locales import use_user_lang

# Logger
logger = logging.getLogger('start_plugin')
logger.setLevel(logging.DEBUG)

# Start komutu - hem özel mesajlarda hem gruplarda çalışacak
@Client.on_message(filters.command(["start", "start@Unoarya_bot"]) & (filters.group | filters.private))
@use_user_lang()
async def start_command(client: Client, message: Message, t):
    """Bot başlatma komutu"""
    try:
        logger.debug(f"Start komutu alındı: {message.text} | Chat ID: {message.chat.id}")
        
        # Kullanıcıyı veritabanına kaydet
        user = await User.get_or_create(id=message.from_user.id)
        
        # Hoşgeldin mesajı
        keyboard = ikb([
            [(t("help"), "help"), (t("settings_text"), "settings")],
            [(t("game_mode"), "help_game")]
        ])
        
        # API limitlerini aşmamak için doğrudan yanıt ver
        await message.reply(
            t("start_text").format(
                name=message.from_user.first_name
            ),
            reply_markup=keyboard,
            quote=True  # API limitlerini aşmamak için
        )
        logger.debug(f"Start komutuna yanıt verildi: {message.chat.id}")
    except Exception as e:
        logger.error(f"Start komutu işlenirken hata: {e}")
        # Hata durumunda basit bir yanıt ver
        await message.reply("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", quote=True)

# Help komutu
@Client.on_message(filters.command(["help", "help@Unoarya_bot"]) & (filters.group | filters.private))
@use_user_lang()
async def help_command_msg(client: Client, message: Message, t):
    """Yardım komutu - mesaj"""
    try:
        logger.debug(f"Help komutu alındı: {message.text} | Chat ID: {message.chat.id}")
        await _help_command(client, message, t)
    except Exception as e:
        logger.error(f"Help komutu işlenirken hata: {e}")
        await message.reply("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", quote=True)

# Help callback
@Client.on_callback_query(filters.regex("^help$"))
@use_user_lang()
async def help_command_cb(client: Client, callback: CallbackQuery, t):
    """Yardım komutu - callback"""
    try:
        logger.debug(f"Help callback alındı | User ID: {callback.from_user.id}")
        await _help_command(client, callback, t)
    except Exception as e:
        logger.error(f"Help callback işlenirken hata: {e}")
        await callback.answer("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

async def _help_command(client: Client, update: Message | CallbackQuery, t):
    """Ortak yardım komutu fonksiyonu"""
    # Klavye oluştur
    keyboard = ikb([
        [(t("game_mode"), "help_game")],
        [(t("back"), "start")]
    ])
    
    # Mesaj içeriği
    text = t("help_message")
    
    # API limitlerini aşmamak için update tipine göre yanıt ver
    if isinstance(update, Message):
        await update.reply(text, reply_markup=keyboard, quote=True)
    else:  # CallbackQuery
        await update.message.edit_text(text, reply_markup=keyboard)
        await update.answer()

# Oyun yardımı
@Client.on_callback_query(filters.regex("^help_game$"))
@use_user_lang()
async def help_game(client: Client, callback: CallbackQuery, t):
    """Oyun yardımı"""
    try:
        logger.debug(f"Help game callback alındı | User ID: {callback.from_user.id}")
        
        # Klavye oluştur
        keyboard = ikb([
            [(t("back"), "help")]
        ])
        
        # Mesaj içeriği
        text = t("game_rules")
        
        # API limitlerini aşmamak için doğrudan yanıt ver
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
    except Exception as e:
        logger.error(f"Help game callback işlenirken hata: {e}")
        await callback.answer("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

# Status komutu
@Client.on_message(filters.command(["status", "status@Unoarya_bot"]) & (filters.group | filters.private))
@use_user_lang()
async def status_command_msg(client: Client, message: Message, t):
    """Durum komutu - mesaj"""
    try:
        logger.debug(f"Status komutu alındı: {message.text} | Chat ID: {message.chat.id}")
        await _status_command(client, message, t)
    except Exception as e:
        logger.error(f"Status komutu işlenirken hata: {e}")
        await message.reply("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", quote=True)

# Status callback
@Client.on_callback_query(filters.regex("^status$"))
@use_user_lang()
async def status_command_cb(client: Client, callback: CallbackQuery, t):
    """Durum komutu - callback"""
    try:
        logger.debug(f"Status callback alındı | User ID: {callback.from_user.id}")
        await _status_command(client, callback, t)
    except Exception as e:
        logger.error(f"Status callback işlenirken hata: {e}")
        await callback.answer("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

async def _status_command(client: Client, update: Message | CallbackQuery, t):
    """Ortak durum komutu fonksiyonu"""
    from unu.db import GameModel
    
    try:
        # Aktif oyun sayısını al
        active_games = await GameModel.filter(status="running").count()
        total_players = 0
        
        # Aktif oyunlardaki toplam oyuncu sayısını hesapla
        if active_games > 0:
            games = await GameModel.filter(status="running").all()
            for game in games:
                total_players += await game.players.all().count()
        
        # Klavye oluştur
        keyboard = ikb([
            [(t("refresh"), "ch_status")],
            [(t("back"), "start")]
        ])
        
        # Mesaj içeriği
        text = t("status_message").format(
            games=active_games,
            players=total_players
        )
        
        # API limitlerini aşmamak için update tipine göre yanıt ver
        if isinstance(update, Message):
            await update.reply(text, reply_markup=keyboard, quote=True)
        else:  # CallbackQuery
            await update.message.edit_text(text, reply_markup=keyboard)
            await update.answer()
    except Exception as e:
        logger.error(f"Status bilgisi alınırken hata: {e}")
        # Hata durumunda basit bir yanıt ver
        text = "Durum bilgisi alınamadı. Lütfen daha sonra tekrar deneyin."
        if isinstance(update, Message):
            await update.reply(text, quote=True)
        else:  # CallbackQuery
            await update.answer(text)

# Status yenileme
@Client.on_callback_query(filters.regex("^ch_status$"))
@use_user_lang()
async def ch_status(client: Client, callback: CallbackQuery, t):
    """Durum yenileme"""
    try:
        logger.debug(f"Status yenileme callback alındı | User ID: {callback.from_user.id}")
        await _status_command(client, callback, t)
    except Exception as e:
        logger.error(f"Status yenileme callback işlenirken hata: {e}")
        await callback.answer("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
