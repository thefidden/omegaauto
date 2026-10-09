import logging
from functools import wraps
from pathlib import Path

import telebot
from django.conf import settings
from telebot.async_telebot import AsyncTeleBot
from telebot.types import KeyboardButton, Message, MessageEntity, ReplyKeyboardMarkup, WebAppInfo

bot = AsyncTeleBot(settings.TELEGRAM_BOT_TOKEN)
telebot.logger.setLevel(logging.CRITICAL)

OPEN_WEB_APP = '🌐 Открыть каталог автомобилей'
PARSE_EMOJI = 'Спарсить эмодзи'
GREETING_IMAGE = Path(settings.MEDIA_ROOT) / 'Telegram Bot Greeting Image.png'

GREETING = '''
<tg-emoji emoji-id="5334607672375254726">👋</tg-emoji> Добро пожаловать в OMEGA AUTO!

<tg-emoji emoji-id="5258396243666681152">🔎</tg-emoji> Подбираем для Вас автомобили в Китае для импорта в Россию, проверяя документы и техническое состояние.

Выберите действие в меню ниже <tg-emoji emoji-id="5294010026585777874">⬇️</tg-emoji>
'''


superuser_id = int(settings.TELEGRAM_SUPERUSER_ID)


def superuser_only(handler):
    @wraps(handler)
    async def wrapped(message: Message, *args, **kwargs):
        if message.from_user is None or message.from_user.id != superuser_id:
            return

        return await handler(message, *args, **kwargs)

    return wrapped


@bot.message_handler(commands = ['start'])
async def start(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard = True)

    open_web_app_button = KeyboardButton(
        OPEN_WEB_APP,
        web_app = WebAppInfo(url = 'https://omegaauto.org/#brand-selection'),
        style = 'primary'
    )
    parse_emoji_button = KeyboardButton(PARSE_EMOJI)

    markup.add(open_web_app_button)

    if message.from_user and message.from_user.id == superuser_id:
        markup.add(parse_emoji_button)

    if GREETING_IMAGE.is_file():
        with GREETING_IMAGE.open('rb') as photo:
            await bot.send_photo(
                chat_id = message.chat.id,
                caption = GREETING,
                photo = photo,
                parse_mode = 'HTML',
                reply_markup = markup
            )
        return

    await bot.send_message(
        chat_id = message.chat.id,
        text = GREETING,
        parse_mode = 'HTML',
        reply_markup = markup
    )


def get_entity_text(text: str, entity: MessageEntity) -> str:
    text_utf16 = text.encode('utf-16-le')
    start = entity.offset * 2
    end = start + entity.length * 2

    return text_utf16[start:end].decode('utf-16-le')


@bot.message_handler(func = lambda message: message.text == PARSE_EMOJI)
@superuser_only
async def parse_emoji_command(message: Message):
    await bot.send_message(
        chat_id = message.chat.id,
        text = 'Отправьте кастомное эмодзи'
    )


@bot.message_handler(
    func = lambda message: any(
        entity.type == 'custom_emoji'
        for entity in message.entities or []
    )
)
@superuser_only
async def parse_custom_emoji(message: Message):
    custom_emojis = [
        (
            entity.custom_emoji_id,
            get_entity_text(message.text, entity)
        )
        for entity in message.entities or []
        if entity.type == 'custom_emoji'
    ]

    text = '\n\n'.join(
        f'ID кастомного эмодзи: `{custom_emoji_id}`\n'
        f'Дефолтное эмодзи: `{default_emoji}`'
        for custom_emoji_id, default_emoji in custom_emojis
    )

    await bot.send_message(
        chat_id = message.chat.id,
        text = text,
        reply_to_message_id = message.message_id,
        parse_mode = 'MarkdownV2'
    )
