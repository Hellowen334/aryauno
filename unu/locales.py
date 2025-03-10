from functools import partial, wraps
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from hydrogram import Client
from hydrogram.enums import ChatType
from hydrogram.types import CallbackQuery, Message

from config import player_game
from unu.db import Chat, User

if TYPE_CHECKING:
    from unu.game import Game


default_language = "tr-TR"


def load_locales() -> dict[str, dict[str, str]]:
    ldict = {}
    for lang_file in Path("locales").glob("*.yml"):
        with lang_file.open(encoding="utf-8") as f:
            ldict[lang_file.stem] = yaml.safe_load(f)

    return ldict


langdict = load_locales()


def use_lang():
    def decorator(func):
        @wraps(func)
        async def wrapper(client: Client, message: CallbackQuery | Message):
            ulang = (await User.get_or_create(id=message.from_user.id))[0].lang
            if not isinstance(message, Message):
                if message.from_user.id not in player_game:
                    clang = ulang
                else:
                    game: Game = player_game[message.from_user.id]
                    chatid = game.chat.id
                    clang = (await Chat.get_or_create(id=chatid))[0].lang
            else:
                clang = (await Chat.get_or_create(id=message.chat.id))[0].lang
            ulfunc = partial(get_locale_string, ulang)
            clfunc = partial(get_locale_string, clang)
            return await func(client, message, ulfunc, clfunc)

        return wrapper

    return decorator


def use_chat_lang():
    def decorator(func):
        @wraps(func)
        async def wrapper(client: Client, message: CallbackQuery | Message):
            mmessage = message.message if not isinstance(message, Message) else message
            if mmessage.chat.type == ChatType.PRIVATE:
                clang = (await User.get_or_create(id=mmessage.chat.id))[0].lang
            else:
                clang = (await Chat.get_or_create(id=mmessage.chat.id))[0].lang
            clfunc = partial(get_locale_string, clang)
            return await func(client, message, clfunc)

        return wrapper

    return decorator


def use_user_lang():
    def decorator(func):
        @wraps(func)
        async def wrapper(client: Client, message: CallbackQuery | Message):
            try:
                ulang = (await User.get_or_create(id=message.from_user.id))[0].lang
                ulfunc = partial(get_locale_string, ulang)
                return await func(client, message, ulfunc)
            except Exception as e:
                import logging
                logging.getLogger('root').error(f"Dil işlenirken hata: {e}")
                # Varsayılan dili kullan
                ulfunc = partial(get_locale_string, default_language)
                return await func(client, message, ulfunc)

        return wrapper

    return decorator


def get_locale_string(language: str, key: str) -> str:
    try:
        if not isinstance(key, str):
            key = str(key)
        
        if language not in langdict:
            language = default_language
            
        result = langdict[language].get(key)
        if result is None:
            result = langdict[default_language].get(key)
        if result is None:
            result = key
            
        return result
    except Exception as e:
        import logging
        logging.getLogger('root').error(f"Dil çevirisi hatası: {e}, dil: {language}, anahtar: {key}")
        return key
